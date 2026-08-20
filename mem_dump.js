// mem_dump.js — 全量内存字符串提取 (rw 段, ASCII>=6, 去重, 限量)
var LF = '/data/data/com.netease.tom/files/mem_dump.txt';
var f = new File(LF, 'a');
function L(s) { try { f.write(s + '\n'); f.flush(); } catch (e) {} }
L('[+] mem_dump ' + Date.now());

var ranges = Process.enumerateRanges('rw-');
var total = 0, out = 0;
var MAX = 15000000;  // 15MB 上限
ranges.forEach(function (r) {
    if (out > MAX) return;
    if (r.size < 4096) return;
    total += r.size;
    try {
        // 分段读 (每段 8MB 内)
        var step = 8 * 1024 * 1024;
        var off = 0;
        while (off < r.size && out <= MAX) {
            var n = Math.min(step, r.size - off);
            var bytes = new Uint8Array(r.base.add(off).readByteArray(n));
            // 提取 ASCII 串
            var cur = '';
            for (var i = 0; i < bytes.length; i++) {
                var c = bytes[i];
                if (c >= 32 && c < 127) {
                    cur += String.fromCharCode(c);
                } else {
                    if (cur.length >= 6) {
                        L(cur);
                        out += cur.length + 1;
                        if (out > MAX) break;
                    }
                    cur = '';
                }
            }
            if (cur.length >= 6) { L(cur); out += cur.length + 1; }
            off += n;
        }
    } catch (e) {}
});
L('[+] total_rw=' + total + ' extracted=' + out + ' done');