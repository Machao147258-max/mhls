// 方案 e: hook malloc (低频稳定) → 捕获解密缓冲 → 8s 后检查明文 → dump
var mallocPtr = Module.findGlobalExportByName('malloc');
var n = 0;
var dir = '/data/user/0/com.netease.tom/files/tomdump';

Interceptor.attach(mallocPtr, {
    onLeave: function (ret) {
        try {
            var sz = this.context.rbx ? 0 : 0;  // x86_64: size 在 rdi, 用 args 取
        } catch (e) {}
    }
});

// 用 onEnter 记录 size
Interceptor.attach(mallocPtr, {
    onEnter: function (args) {
        this.sz = args[0].toInt32();
    },
    onLeave: function (ret) {
        var sz = this.sz;
        if (sz > 1000 && sz < 4 * 1024 * 1024 && n < 200) {
            var p = ret, idx = n++;
            setTimeout(function () {
                try {
                    var b = Array.prototype.slice.call(new Uint8Array(p.readByteArray(16)));
                    var isCipher = (b[0] === 0x58 && b[1] === 0x31 && b[2] === 0x56 && b[3] === 0x35);
                    if (!isCipher) {
                        var hx = '';
                        for (var i = 0; i < 8 && i < b.length; i++) hx += ('0' + b[i].toString(16)).slice(-2);
                        if (b[0] !== 0x00 && hx !== 'ffffffffffffffff') {
                            var full = p.readByteArray(sz);
                            if (full) {
                                try {
                                    var f = new File(dir + '/m_' + idx + '_' + sz + '.bin', 'w');
                                    f.write(full);
                                    f.close();
                                    console.log('★MALLOC-DUMP m_' + idx + '_' + sz + '.bin head=' + hx);
                                } catch (e) {
                                    console.log('★CANDIDATE m_' + idx + '_' + sz + ' head=' + hx);
                                }
                            }
                        }
                    }
                } catch (e) {}
            }, 8000);
        }
    }
});
console.log('OK-MALLOC')