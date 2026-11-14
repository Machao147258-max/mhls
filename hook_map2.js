// map2: malloc 只记录 >=8192 的大缓冲; free 时: map 内完整 dump, map 外 8KB 窗口 (1b4c 明文 / X1V5 密文)
var mallocPtr = Module.findGlobalExportByName('malloc');
var freePtr = Module.findGlobalExportByName('free');
var big = new Map();
var dir = '/data/user/0/com.netease.tom/files';
var cnt = 0;

Interceptor.attach(mallocPtr, {
    onEnter: function (args) {
        this.sz = args[0].toInt32();
    },
    onLeave: function (ret) {
        var sz = this.sz;
        if (sz >= 8192 && sz < 8 * 1024 * 1024 && big.size < 3000) {
            try { big.set(ret.toString(), sz); } catch (e) {}
        }
    }
});

Interceptor.attach(freePtr, {
    onEnter: function (args) {
        var p = args[0];
        if (p.isNull()) return;
        if (cnt > 8000) return;
        var key = p.toString();
        var sz = big.get(key);
        if (sz) big.delete(key);
        try {
            var h = p.readByteArray(8);
            if (!h) return;
            var a = Array.prototype.slice.call(new Uint8Array(h));
            if (a[0] === 0x1b && a[1] === 0x4c) {
                var idx = cnt++;
                var n = sz ? sz : 8192;
                var full = p.readByteArray(n);
                if (full) {
                    try {
                        var f = new File(dir + '/F_' + idx + '_' + n + '.bin', 'w');
                        f.write(full);
                        f.close();
                        console.log('★F_' + idx + '_' + n + (sz ? ' FULL' : ''));
                    } catch (e) {}
                }
            } else if (a[0] === 0x58 && a[1] === 0x31 && a[2] === 0x56 && a[3] === 0x35) {
                var idx = cnt++;
                var n = sz ? sz : 8192;
                var full = p.readByteArray(n);
                if (full) {
                    try {
                        var f = new File(dir + '/C_' + idx + '_' + n + '.bin', 'w');
                        f.write(full);
                        f.close();
                    } catch (e) {}
                }
            }
        } catch (e) {}
    }
});
console.log('OK-MAP2')