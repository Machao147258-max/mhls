// mem_probe.js — 动态内存捕捉: 扫描 rw 段找明文数据驻留
var LF = '/data/data/com.netease.tom/files/mem_probe.txt';
var f = new File(LF, 'a');
function L(s) { try { f.write(s + '\n'); f.flush(); } catch (e) {} }
L('[+] mem_probe ' + Date.now());

var needles = [
    ['drpf', 'h18.drpf.x.netease.com'],
    ['unisec', 'unisec-inner.nie.netease.com'],
    ['udid', '8e066e23b43ea4e3'],
    ['role', '248850489'],
    ['json', 'role_id'],
    ['http', 'POST /'],
    ['host', 'Host: h18']
];
var found = {};
// 只扫可读写的匿名堆段 + 数据段 (限大小)
var ranges = Process.enumerateRanges('rw-');
var scanned = 0, hits = 0;
ranges.forEach(function (r) {
    if (r.size > 64 * 1024 * 1024) return;   // 跳过超大段
    if (r.size < 4096) return;
    scanned++;
    try {
        needles.forEach(function (n) {
            var res = Memory.scanSync(r.base, r.size, n[1]);
            res.forEach(function (m) {
                hits++;
                found[n[0]] = m.address;
                L('[HIT] ' + n[0] + ' @ ' + m.address + ' in ' + r.protection + ' ' + r.size);
            });
        });
    } catch (e) {}
});
L('[+] scanned=' + scanned + ' hits=' + hits);
// 对命中地址 dump 周边 ±512 (明文上下文)
Object.keys(found).forEach(function (k) {
    try {
        var a = found[k];
        var buf = a.sub(256).readByteArray(1024);
        var bytes = new Uint8Array(buf);
        var s = '';
        for (var i = 0; i < bytes.length; i++) {
            var c = bytes[i];
            s += (c >= 32 && c < 127) ? String.fromCharCode(c) : '.';
        }
        L('[DUMP:' + k + '] ' + s);
    } catch (e) {}
});
L('[+] done');