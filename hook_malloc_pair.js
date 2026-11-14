// 配对版: malloc 缓冲 立即读(X1V5=存密文) + 8s 后读(1b4c=存明文) → 密文/明文对
var mallocPtr = Module.findGlobalExportByName('malloc');
var n = 0;
var dir = '/data/user/0/com.netease.tom/files';

Interceptor.attach(mallocPtr, {
    onEnter: function (args) {
        this.sz = args[0].toInt32();
    },
    onLeave: function (ret) {
        var sz = this.sz;
        if (sz > 500 && n < 3000) {
            var p = ret, idx = n++;
            // 2s 后读: 密文 X1V5fzTo? (文件读入后)
            setTimeout(function () {
                try {
                    var h0 = p.readByteArray(8);
                    if (h0) {
                        var a = Array.prototype.slice.call(new Uint8Array(h0));
                        if (a[0] === 0x58 && a[1] === 0x31 && a[2] === 0x56 && a[3] === 0x35) {
                            var full0 = p.readByteArray(Math.min(sz, 262144));
                            if (full0) {
                                try {
                                    var f0 = new File(dir + '/C_' + idx + '_' + sz + '.bin', 'w');
                                    f0.write(full0);
                                    f0.close();
                                    console.log('★CIPHER C_' + idx + '_' + sz);
                                } catch (e) {}
                            }
                        }
                    }
                } catch (e) {}
            }, 2000);
            setTimeout(function () {
                try {
                    var b = Array.prototype.slice.call(new Uint8Array(p.readByteArray(8)));
                    if (b[0] === 0x1b && b[1] === 0x4c) {
                        var full = p.readByteArray(Math.min(sz, 262144));
                        if (full) {
                            try {
                                var f = new File(dir + '/P_' + idx + '_' + sz + '.bin', 'w');
                                f.write(full);
                                f.close();
                                console.log('☆PLAIN P_' + idx + '_' + sz);
                            } catch (e) {}
                        }
                    }
                } catch (e) {}
            }, 2000);
            setTimeout(function () {
                try {
                    var b = Array.prototype.slice.call(new Uint8Array(p.readByteArray(8)));
                    if (b[0] === 0x1b && b[1] === 0x4c) {
                        var full = p.readByteArray(Math.min(sz, 262144));
                        if (full) {
                            try {
                                var f = new File(dir + '/P_' + idx + '_' + sz + '.bin', 'w');
                                f.write(full);
                                f.close();
                                console.log('☆PLAIN2 P_' + idx + '_' + sz);
                            } catch (e) {}
                        }
                    }
                } catch (e) {}
            }, 8000);
        }
    }
});
console.log('OK-PAIR')