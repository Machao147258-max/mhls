// 终极捕获: onLeave 内 setTimeout(6s) → dump dst 完整明文到 app 目录
// hook_capture2 已验证此模式 (LATE-DST 命中 TSYS 明文)
var memcpy = Module.findGlobalExportByName('memcpy');
var n = 0;
var dir = '/data/user/0/com.netease.tom/files/tomdump';

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 600) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    if (h[0] === 0x58 && h[1] === 0x31 && h[2] === 0x56 && h[3] === 0x35) {
                        var dst = this.dst, sz = this.n, idx = n++;
                        setTimeout(function () {
                            try {
                                var b = Array.prototype.slice.call(new Uint8Array(dst.readByteArray(16)));
                                var isCipher = (b[0] === 0x58 && b[1] === 0x31 && b[2] === 0x56 && b[3] === 0x35);
                                if (!isCipher && b[0] !== 0x00 && b[0] !== 0xff) {
                                    var full = dst.readByteArray(sz);
                                    if (full) {
                                        try {
                                            var f = new File(dir + '/p_' + idx + '_' + sz + '.bin', 'w');
                                            f.write(full);
                                            f.close();
                                            console.log('★SAVED p_' + idx + '_' + sz + '.bin');
                                        } catch (e) {
                                            console.log('★PLAIN n=' + sz + ' head=' + hex16(b) + ' write-fail');
                                        }
                                    }
                                } else if (!isCipher) {
                                    console.log('★PLAIN n=' + sz + ' head=' + hex16(b));
                                }
                            } catch (e) {}
                        }, 6000);
                    }
                }
            } catch (e) {}
        }
    }
});

function hex16(arr) {
    var s = '';
    for (var i = 0; i < 16 && i < arr.length; i++) s += ('0' + arr[i].toString(16)).slice(-2);
    return s;
}
console.log('OK-FINAL2 dir=' + dir)