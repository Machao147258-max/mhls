// 终极: hook 捕获 X1V5fzTo → 8s 后 dump src (解密原地明文) 到 app 私有目录
// 防洪峰: 只处理 >4000B 的拷贝 + 频率限制 (每 200ms 最多 1 个)
var memcpy = Module.findGlobalExportByName('memcpy');
var n = 0, lastT = 0;
var dir = '/data/user/0/com.netease.tom/files/tomdump';
try { var t = new File(dir, 'w'); t.close(); } catch (e) { dir = '/data/local/tmp'; }

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        var now = Date.now();
        if (this.n > 4000 && now - lastT > 200 && n < 300) {
            lastT = now;
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    if (h[0] === 0x58 && h[1] === 0x31 && h[2] === 0x56 && h[3] === 0x35) {
                        var src = this.src, sz = this.n, idx = n++;
                        setTimeout(function () {
                            try {
                                var b2 = Array.prototype.slice.call(new Uint8Array(src.readByteArray(16)));
                                var isCipher = (b2[0] === 0x58 && b2[1] === 0x31 && b2[2] === 0x56 && b2[3] === 0x35);
                                if (!isCipher && b2[0] !== 0x00) {
                                    var full = src.readByteArray(sz);
                                    if (full) {
                                        var f = new File(dir + '/p_' + idx + '_' + sz + '.bin', 'w');
                                        f.write(full);
                                        f.close();
                                        console.log('★SAVED p_' + idx + '_' + sz + '.bin ' + dir);
                                    }
                                }
                            } catch (e) {}
                        }, 8000);
                    }
                }
            } catch (e) {}
        }
    }
});
console.log('OK-FINAL-DUMP dir=' + dir);