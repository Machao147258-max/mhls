// 修正版: dump 到 files/ 根 (必存在) + 错误可见 + 上限 400
var mallocPtr = Module.findGlobalExportByName('malloc');
var n = 0;
var dir = '/data/user/0/com.netease.tom/files';

Interceptor.attach(mallocPtr, {
    onEnter: function (args) {
        this.sz = args[0].toInt32();
    },
    onLeave: function (ret) {
        var sz = this.sz;
        if (sz > 500 && n < 400) {
            var p = ret, idx = n++;
            setTimeout(function () {
                try {
                    var b = Array.prototype.slice.call(new Uint8Array(p.readByteArray(8)));
                    if (b[0] === 0x1b && b[1] === 0x4c) {  // \x1bL
                        var hx = '';
                        for (var i = 0; i < 8; i++) hx += ('0' + b[i].toString(16)).slice(-2);
                        var full = p.readByteArray(sz);
                        if (full) {
                            try {
                                var f = new File(dir + '/L_' + idx + '_' + sz + '.bin', 'w');
                                f.write(full);
                                f.close();
                                console.log('★SAVED L_' + idx + '_' + sz + '.bin ' + hx);
                            } catch (e) {
                                console.log('★★WRITE-FAIL L_' + idx + '_' + sz + ': ' + e);
                            }
                        }
                    }
                } catch (e) {}
            }, 8000);
        }
    }
});
console.log('OK-MALLOC-FIX')