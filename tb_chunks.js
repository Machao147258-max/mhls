// tb_chunks: 低噪抓取 —— 逐 chunk 边界解析,只读合法跨度,打包写入单一文件
function log(m) { console.log(m); }

var PACK = '/data/data/com.netease.tom/cache/chunks_pack.bin';
var HEADER_LEN = 12;
var MAX_HITS = 120;
var MAX_CHUNK = 4 * 1024 * 1024;

// 在 JS 里按 Lua 5.1 格式走一遍,算出 chunk 结束偏移;失败返回 null
function walkChunkEnd(base, start, rangeEnd) {
    function u8(o) { return Memory.readU8(base.add(o)); }
    function u32(o) { return Memory.readU32(base.add(o)); }
    function need(o, n) { if (start + o + n > rangeEnd) throw new Error('bounds'); }

    var p = start;
    function readStr() {
        need(p - start, 4);
        var l = u32(p - start); p += 4;
        if (l > 4096 || l < 0) throw new Error('strlen');
        need(p - start, l);
        var s = l > 1 ? Memory.readCString(base.add(p), l - 1) : '';
        p += l;
        return s;
    }
    function walkFn() {
        need(p - start, 4);
        var sname = readStr();
        need(p - start, 8); p += 8;             // linedefined, lastlinedefined
        need(p - start, 4); p += 4;             // nups, params, isvararg, maxstack
        var n = u32(p - start); p += 4;
        if (n > 1 << 22) throw new Error('code');
        need(p - start, n * 4); p += n * 4;
        n = u32(p - start); p += 4;
        if (n > 1 << 20) throw new Error('const');
        for (var i = 0; i < n; i++) {
            need(p - start, 1);
            var t = u8(p - start); p += 1;
            if (t === 0) continue;
            if (t === 1) { need(p - start, 1); p += 1; continue; }
            if (t === 3) { need(p - start, 8); p += 8; continue; }
            if (t === 4) { readStr(); continue; }
            throw new Error('ctype ' + t);
        }
        n = u32(p - start); p += 4;
        if (n > 1 << 20) throw new Error('upv');
        need(p - start, n * 2); p += n * 2;
        n = u32(p - start); p += 4;
        if (n > 1 << 20) throw new Error('proto');
        for (var j = 0; j < n; j++) walkFn();
        return sname;
    }
    var topName = walkFn();
    return { end: p, name: topName };
}

setTimeout(function () {
    log('[*] tb_chunks attach ok');
    var pat = '1b 4c 75 61 51';
    var all = [];

    Process.enumerateRanges('rw-').forEach(function (r) {
        if (all.length >= MAX_HITS) return;
        if (r.size > 128 * 1024 * 1024) return;
        var hits = null;
        try { hits = Memory.scanSync(r.base, r.size, pat); } catch (e) { return; }
        hits.forEach(function (h) {
            if (all.length >= MAX_HITS) return;
            var off = h.address.sub(r.base).toInt32();
            if (off + HEADER_LEN + 8 > r.size) return;
            // 头尾校验: 51 00 01 04 04 04 08 00
            var tail = new Uint8Array(r.base.add(off + 4).readByteArray(8));
            var expect = [0x51, 0x00, 0x01, 0x04, 0x04, 0x04, 0x08, 0x00];
            var ok = true;
            for (var i = 0; i < 8; i++) { if (tail[i] !== expect[i]) { ok = false; break; } }
            if (!ok) return;
            var parsed = null;
            try { parsed = walkChunkEnd(r.base, off + HEADER_LEN, r.size); }
            catch (e) { return; }
            var size = parsed.end - off - HEADER_LEN + HEADER_LEN;
            var chunkStart = off;
            var chunkSize = parsed.end - chunkStart;
            if (chunkSize <= HEADER_LEN || chunkSize > MAX_CHUNK) return;
            all.push({ addr: h.address, name: parsed.name, chunkStart: chunkStart, chunkSize: chunkSize, base: r.base });
        });
    });

    log('[+] 解析成功 ' + all.length + ' 个 chunk');
    if (!all.length) { log('[*] 暂无(等加载后再跑一次)'); return; }

    // 打包写入: 'TLC1' + 条目数 + [u32 nameLen, name, u32 size, data]*
    var out = [];
    var idx = 0;
    all.forEach(function (c) {
        var nb = Memory.readByteArray(c.base.add(c.chunkStart), c.chunkSize);
        out.push({ name: c.name, buf: nb });
    });

    var f = new File(PACK, 'wb');
    f.write('TLC1');
    var head = new ArrayBuffer(4);
    new DataView(head).setUint32(0, out.length, true);
    f.write(head);
    out.forEach(function (o) {
        var nbuf = new ArrayBuffer(4 + o.name.length);
        var dv = new DataView(nbuf);
        dv.setUint32(0, o.name.length, true);
        for (var i = 0; i < o.name.length; i++) dv.setUint8(4 + i, o.name.charCodeAt(i) & 0xff);
        f.write(nbuf);
        var sbuf = new ArrayBuffer(4);
        new DataView(sbuf).setUint32(0, o.buf.byteLength, true);
        f.write(sbuf);
        f.write(o.buf);
        log('  [+] ' + o.name + '  ' + o.buf.byteLength + 'B');
    });
    f.close();
    log('[*] 已打包: ' + PACK);
}, 15000);