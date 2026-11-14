// tb_probe4: 全可读内存(rw-/r--/r-x)扫 Lua 头,按保护类型统计 + 采样
function log(m) { console.log(m); }
setTimeout(function () {
    log('[*] tb_probe4 attach ok');
    var pat = '1b 4c 75 61 51';
    var byProt = { 'rw-': 0, 'r--': 0, 'r-x': 0, 'other': 0 };
    var samples = [];
    ['rw-', 'r--', 'r-x'].forEach(function (prot) {
        var ranges = Process.enumerateRanges(prot);
        ranges.forEach(function (r) {
            if (r.size > 256 * 1024 * 1024) return;
            var hits = null;
            try { hits = Memory.scanSync(r.base, r.size, pat); } catch (e) { return; }
            byProt[prot] += hits.length;
            if (samples.length < 12 && hits.length) {
                hits.slice(0, 2).forEach(function (h) {
                    var b = h.address.readByteArray(64);
                    var hex = Array.from(new Uint8Array(b)).slice(0, 40).map(function (x) { return x.toString(16).padStart(2, '0'); }).join(' ');
                    samples.push(prot + ' @' + h.address + ' size=' + r.size + '\n      ' + hex);
                });
            }
        });
    });
    log('[+] 命中: rw-=' + byProt['rw-'] + ' r--=' + byProt['r--'] + ' r-x=' + byProt['r-x']);
    samples.forEach(function (s) { log('  ' + s); });
    log('[*] done');
}, 3000);