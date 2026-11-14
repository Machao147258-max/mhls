// malloc+free 联合: malloc 记 ptr→size; free 时查 map 完整 dump (明文 F_ / 密文 FC_)
var mallocPtr = Module.findGlobalExportByName('malloc');
var freePtr = Module.findGlobalExportByName('free');
var sizes = new Map();
var dir = '/data/user/0/com.netease.tom/files';

Interceptor.attach(mallocPtr, {
    onEnter: function (args) {
        this.sz = args[0].toInt32();
    },
    onLeave: function (ret) {
        if (this.sz >= 300) {
            try { sizes.set(ret.toString(), this.sz); } catch (e) {}
        }
    }
});

Interceptor.attach(freePtr, {
    onEnter: function (args) {
        var p = args[0];
        if (p.isNull()) return;
        var key = p.toString();
        var sz = sizes.get(key);
        if (!sz) return;
        sizes.delete(key);
        if (sz > 8192 * 4) return;  // 跳过超大 (非脚本)
        try {
            var h = p.readByteArray(8);
            if (!h) return;
            var a = Array.prototype.slice.call(new Uint8Array(h));
            var fname = null;
            if (a[0] === 0x1b && a[1] === 0x4c) fname = '/F_' + sz + '_' + key.slice(2);
            else if (a[0] === 0x58 && a[1] === 0x31 && a[2] === 0x56 && a[3] === 0x35) fname = '/FC_' + sz + '_' + key.slice(2);
            if (fname) {
                var full = p.readByteArray(sz);
                if (full) {
                    try {
                        var f = new File(dir + fname + '.bin', 'w');
                        f.write(full);
                        f.close();
                        console.log('★' + fname);
                    } catch (e) {}
                }
            }
        } catch (e) {}
    }
});
console.log('OK-MAP')