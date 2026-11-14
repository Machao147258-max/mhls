// free-hook 版: hook free onEnter 读缓冲头 → 1b4c 存明文 / X1V5 存密文 (释放即捕获, 零定时器)
var freePtr = Module.findGlobalExportByName('free');
var n = 0;
var dir = '/data/user/0/com.netease.tom/files';

Interceptor.attach(freePtr, {
    onEnter: function (args) {
        var p = args[0];
        if (p.isNull()) return;
        if (n < 4000) {
            try {
                var h = p.readByteArray(8);
                if (h) {
                    var a = Array.prototype.slice.call(new Uint8Array(h));
                    if (a[0] === 0x1b && a[1] === 0x4c) {
                        // 明文! 读大小: 需要知道缓冲大小 —— 从 luac 结构估算: 读远一点 (min 4KB)
                        var idx = n++;
                        var full = p.readByteArray(8192);
                        if (full) {
                            try {
                                var f = new File(dir + '/F_' + idx + '.bin', 'w');
                                f.write(full);
                                f.close();
                                console.log('★LUAC-FREE F_' + idx + ' @' + p);
                            } catch (e) {}
                        }
                    } else if (a[0] === 0x58 && a[1] === 0x31 && a[2] === 0x56 && a[3] === 0x35) {
                        var idx = n++;
                        var full = p.readByteArray(8192);
                        if (full) {
                            try {
                                var f = new File(dir + '/FC_' + idx + '.bin', 'w');
                                f.write(full);
                                f.close();
                            } catch (e) {}
                        }
                    }
                }
            } catch (e) {}
        }
    }
});
console.log('OK-FREE')