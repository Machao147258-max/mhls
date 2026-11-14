// hook_scan3.js — 找到 DELTA 后 hook 核心入口 + 周边函数入口, 抓寄存器
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'w');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] 脚本启动 ' + Date.now());
function hex(b) {
    var s = "";
    for (var i = 0; i < b.length; i++) s += ("0" + b[i].toString(16)).slice(-2);
    return s;
}
function toStr(b) {
    var s = "";
    for (var i = 0; i < b.length; i++) {
        var c = b[i];
        s += (c >= 32 && c < 127) ? String.fromCharCode(c) : ".";
    }
    return s;
}
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.replace(p, new NativeCallback(function () {
            L('[防自杀] ' + n);
            return 0;
        }, 'int', ['int']));
        L('[+] 防自杀 ' + n);
    } catch (e) { L('[-] ' + n + ': ' + e); }
});
function dumpRegs(tag, ctx) {
    try {
        var regs = { rsi: ctx.rsi, rdx: ctx.rdx, rcx: ctx.rcx, r8: ctx.r8, r9: ctx.r9, r14: ctx.r14, r15: ctx.r15, rdi: ctx.rdi };
        var line = '[REG ' + tag + '] ';
        for (var k in regs) {
            line += k + '=' + regs[k] + ' ';
        }
        L(line);
        // 尝试读 rsi/rdx/rcx/r8 为 16B key
        ['rsi', 'rdx', 'rcx', 'r8', 'r9', 'r14'].forEach(function (rn) {
            try {
                var p = regs[rn];
                if (p && !p.isNull()) {
                    var kb = p.readByteArray(16);
                    var s = toStr(kb);
                    // 只记录"低熵"或含可打印的
                    var printable = 0;
                    for (var i = 0; i < 16; i++) if (s.charCodeAt(i) !== 46) printable++;
                    if (printable >= 4 || kb[0] === 0x1b) {
                        L('[★MEM ' + rn + '] ' + JSON.stringify(s) + ' hex=' + hex(kb));
                    }
                }
            } catch (e) {}
        });
    } catch (e) { L('[reg err] ' + e); }
}
var done = false;
var tries = 0;
var iv = setInterval(function () {
    if (done) return;
    tries++;
    try {
        var ranges = Process.enumerateRanges('rwx');
        var target = null;
        var found = false;
        for (var ri = 0; ri < ranges.length && !found; ri++) {
            var r = ranges[ri];
            if (r.size > 0x20000000) continue;
            Memory.scan(r.base, r.size, 'b9 79 37 9e', {
                onMatch: function (addr) {
                    if (!found) {
                        found = true;
                        target = addr;
                    }
                },
                onComplete: function () {}
            });
            // 同步等? 不——扫描是异步的, 用 scanSync
        }
    } catch (e) { L('[scan err] ' + e); }
    // 用 scanSync 同步扫描 (frida 有 Memory.scanSync?)
    try {
        var ranges2 = Process.enumerateRanges('rwx');
        for (var ri2 = 0; ri2 < ranges2.length; ri2++) {
            var r2 = ranges2[ri2];
            if (r2.size > 0x20000000) continue;
            var hits = Memory.scanSync(r2.base, r2.size, 'b9 79 37 9e');
            if (hits.length > 0) {
                L('[★DELTA] ' + hits[0].address);
                // hook DELTA 核心入口 (往前找 push rbp / sub rsp)
                var core = hits[0].address.sub(0x140);
                var ent = Memory.scanSync(core, 0x140, '55');
                var hookedAny = false;
                for (var ei = 0; ei < ent.length; ei++) {
                    var e = ent[ei].address;
                    try {
                        Interceptor.attach(e, {
                            onEnter: function () {
                                dumpRegs('core', this.context);
                            }
                        });
                        L('[+] core hook @' + e);
                        hookedAny = true;
                    } catch (ex) {}
                    if (hookedAny) break;
                }
                // 也 hook DELTA 本身
                try {
                    Interceptor.attach(hits[0].address, {
                        onEnter: function () { dumpRegs('delta', this.context); }
                    });
                    L('[+] delta hook OK');
                } catch (e) { L('[-] delta: ' + e); }
                done = true;
                clearInterval(iv);
                L('[+] 就绪, 等待解密...');
                return;
            }
        }
    } catch (e) {
        if (tries % 5 === 0) L('[scanSync err] ' + e);
    }
    if (tries > 120) { clearInterval(iv); L('[-] 120s 超时'); }
}, 1000);
