// tb_harvest: 护盾(反处决) + 低噪 Lua chunk 抓取一体化
// 用法: frida -H 127.0.0.1:31337 -p <PID> -l tb_harvest.js
function log(m) { console.log(m); }

var PACK = '/data/data/com.netease.tom/cache/chunks_pack.bin';
var myPid = -1, suppressed = 0;
var SUS = /trace|stack|guard|watch|sec|anti|detect|dTi/i;
var FATAL = { 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 11: 1 };

function tidName(tid) {
    try {
        var t = Process.enumerateThreads().find(function (x) { return x.id === tid; });
        return t ? t.name : '?';
    } catch (e) { return '?'; }
}
function isSusp(tid) { var n = tidName(tid); return SUS.test(n) || /^\w{1,3}$/.test(n); }

// ---------- 护盾 ----------
function installGuard() {
    function mkKill(orig, kind) {
        return function (a, b, c) {
            var pid = a, sig = b;
            if (kind === 'tgkill') { pid = a; sig = c; }
            if (kind === 'pthread_kill') { pid = myPid; sig = b; }
            if (kind === 'raise') { pid = myPid; sig = a; }
            var tid = Process.getCurrentThreadId();
            if ((pid === myPid || pid === 0) && FATAL[sig]) {
                suppressed++;
                log('[guard] 吞信号 ' + sig + ' <- tid=' + tid + ' (' + tidName(tid) + ') #' + suppressed);
                return 0;
            }
            try {
                if (kind === 'tgkill') return orig(a, b, c);
                if (kind === 'pthread_kill') return orig(a, b);
                return orig(pid, sig);
            } catch (e) { return 0; }
        };
    }
    [['kill', 'kill'], ['tgkill', 'tgkill'], ['pthread_kill', 'pthread_kill'], ['raise', 'raise']].forEach(function (p) {
        try {
            var a = Module.findGlobalExportByName(p[0]);
            if (a.isNull()) return;
            var o = new NativeFunction(a, 'int', ['int', 'int', 'int']);
            Interceptor.replace(a, new NativeCallback(mkKill(o, p[1]), 'int', ['int', 'int', 'int']));
            log('[+] guard ' + p[0]);
        } catch (e) { log('[-] ' + p[0] + ': ' + e); }
    });
    [['abort'], ['exit'], ['_exit']].forEach(function (p) {
        try {
            var a = Module.findGlobalExportByName(p[0]);
            if (a.isNull()) return;
            var o = new NativeFunction(a, 'void', ['int']);
            Interceptor.replace(a, new NativeCallback(function (code) {
                var tid = Process.getCurrentThreadId();
                if (isSusp(tid)) {
                    suppressed++;
                    log('[guard] 拦 ' + p[0] + ' <- tid=' + tid + ' (' + tidName(tid) + ') #' + suppressed);
                    while (true) { Thread.sleep(1); }
                }
                try { o(code); } catch (e) {}
            }, 'void', ['int']));
            log('[+] guard ' + p[0]);
        } catch (e) { log('[-] ' + p[0] + ': ' + e); }
    });
}

// ---------- 抓取 ----------
function walkEnd(base, start, rangeEnd) {
    var p = start;
    function need(n) { if (start + n > rangeEnd) throw new Error('b'); }
    function u8(o) { return Memory.readU8(base.add(o)); }
    function u32(o) { return Memory.readU32(base.add(o)); }
    function rs() {
        need(4); var l = u32(p); p += 4;
        if (l > 4096 || l < 0) throw new Error('sl');
        need(l);
        var s = l > 1 ? Memory.readCString(base.add(p), l - 1) : '';
        p += l;
        return s;
    }
    function fn() {
        var s = rs();
        need(8); p += 8;
        need(4); p += 4;
        var n = u32(p); p += 4;
        if (n > (1 << 22)) throw new Error('c');
        need(n * 4); p += n * 4;
        n = u32(p); p += 4;
        if (n > (1 << 20)) throw new Error('k');
        for (var i = 0; i < n; i++) {
            need(1); var t = u8(p); p += 1;
            if (t === 0) continue;
            if (t === 1) { need(1); p += 1; continue; }
            if (t === 3) { need(8); p += 8; continue; }
            if (t === 4) { rs(); continue; }
            throw new Error('t' + t);
        }
        n = u32(p); p += 4; if (n > (1 << 24)) throw new Error('li');
        need(n); p += n;
        n = u32(p); p += 4; if (n > (1 << 20)) throw new Error('lv');
        for (var j = 0; j < n; j++) { rs(); need(8); p += 8; }
        n = u32(p); p += 4; if (n > (1 << 20)) throw new Error('uv');
        for (var k2 = 0; k2 < n; k2++) rs();
        n = u32(p); p += 4; if (n > (1 << 20)) throw new Error('pr');
        for (var k3 = 0; k3 < n; k3++) fn();
        return s;
    }
    return fn();
}

function scanAndPack(tag) {
    var found = [];
    Process.enumerateRanges('rw-').forEach(function (r) {
        if (r.size > 128 * 1024 * 1024) return;
        var hits = null;
        try { hits = Memory.scanSync(r.base, r.size, '1b 4c 75 61 51'); } catch (e) { return; }
        hits.forEach(function (h) {
            if (found.length >= 150) return;
            var off = h.address.sub(r.base).toInt32();
            if (off + 20 > r.size) return;
            var tail = new Uint8Array(r.base.add(off + 4).readByteArray(8));
            var ok = true, exp = [0x51, 0, 1, 4, 4, 4, 8, 0];
            for (var i = 0; i < 8; i++) if (tail[i] !== exp[i]) { ok = false; break; }
            if (!ok) return;
            var nm = null, end = null;
            try { end = walkEnd(r.base, off + 12, r.size); nm = Memory.readCString(r.base.add(off + 16), 200); } catch (e) { return; }
            var size = end - off;
            if (size <= 12 || size > 4 * 1024 * 1024) return;
            found.push({ name: nm, off: off, size: size, base: r.base });
        });
    });
    log('[harvest ' + tag + '] 解析到 ' + found.length + ' 个 chunk');
    if (!found.length) return;
    var seen = {};
    var uniq = found.filter(function (c) { var k = c.base.toString() + ':' + c.off; if (seen[k]) return false; seen[k] = true; return true; });
    try {
        var f = new File(PACK, 'wb');
        f.write('TLC1');
        var hd = new ArrayBuffer(4); new DataView(hd).setUint32(0, uniq.length, true);
        f.write(hd);
        uniq.forEach(function (c) {
            var buf = c.base.add(c.off).readByteArray(c.size);
            var nm = c.name || 'chunk';
            var nh = new ArrayBuffer(4 + nm.length);
            var dv = new DataView(nh);
            dv.setUint32(0, nm.length, true);
            for (var i = 0; i < nm.length; i++) dv.setUint8(4 + i, nm.charCodeAt(i) & 0xff);
            f.write(nh);
            var sh = new ArrayBuffer(4); new DataView(sh).setUint32(0, c.size, true);
            f.write(sh); f.write(buf);
        });
        f.close();
        log('[harvest ' + tag + '] 已打包 ' + uniq.length + ' 个 → ' + PACK);
    } catch (e) { log('[-] 打包失败: ' + e); }
}

setTimeout(function () {
    myPid = Process.id;
    log('[*] tb_harvest pid=' + myPid);
    installGuard();
    log('[*] 开始定时抓取(15s/45s/90s 三趟)');
    setTimeout(function () { scanAndPack('T1'); }, 15000);
    setTimeout(function () { scanAndPack('T2'); }, 45000);
    setTimeout(function () { scanAndPack('T3'); }, 90000);
    setInterval(function () {}, 1000);
}, 2000);