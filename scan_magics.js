// 纯读扫描: Memory.scan (native 快扫) 找明文 luac 魔数 → dump
// 明文魔数 (从 20113 实证): 59ad5483 d3139566 b5720000 b2720000 c8114dd0 018d841b 9181841b
var magics = [
    ['59ad5483', '59 ad 54 83'],
    ['d3139566', 'd3 13 95 66'],
    ['b5720000', 'b5 72 00 00'],
    ['b2720000', 'b2 72 00 00'],
    ['c8114dd0', 'c8 11 4d d0'],
    ['018d841b', '01 8d 84 1b'],
    ['9181841b', '91 81 84 1b']
];
var dir = '/data/user/0/com.netease.tom/files/tomdump';
try { var t = new File(dir, 'w'); t.close(); } catch (e) { dir = '/data/local/tmp'; }
var found = 0;

var ranges = Process.enumerateRanges('rw-').filter(function (r) {
    return r.size > 1024 * 1024 && r.size < 128 * 1024 * 1024;
});
console.log('ranges=' + ranges.length);

ranges.forEach(function (r, ri) {
    magics.forEach(function (m) {
        try {
            Memory.scan(r.base, r.size, m[1], {
                onMatch: function (addr, size) {
                    found++;
                    console.log('★MATCH ' + m[0] + ' @' + addr + ' range#' + ri);
                    if (found <= 30) {
                        try {
                            var off = 4;
                            var f = new File(dir + '/luac_' + m[0] + '_' + addr.toString(16) + '.bin', 'w');
                            // dump 512KB 窗口 (地址+偏移对齐)
                            var dumpSize = 512 * 1024;
                            var base = addr.sub(0x100);  // 前 256B 上下文
                            var b = base.readByteArray(dumpSize);
                            if (b) f.write(b);
                            f.close();
                            // 读前 32 字节打印
                            var h = addr.readByteArray(32);
                            if (h) {
                                var arr = Array.prototype.slice.call(new Uint8Array(h));
                                var hs = '';
                                for (var i = 0; i < arr.length; i++) hs += ('0' + arr[i].toString(16)).slice(-2);
                                console.log('  HEAD: ' + hs.slice(0, 40));
                            }
                        } catch (e) { console.log('  dump fail: ' + e); }
                    }
                },
                onComplete: function () {}
            });
        } catch (e) {}
    });
});
console.log('SCAN-DONE found=' + found)