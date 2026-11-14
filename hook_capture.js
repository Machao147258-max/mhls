// 捕获 X1V5fzTo 密文 + 同步读 dst 明文 (无 setInterval, 输出到 stdout 由 -o 落盘)
// 用法: frida -p <pid> -l hook_capture.js
var memcpy = Module.findGlobalExportByName('memcpy');
var c = 0;

function hex(b, n) {
    var out = '';
    for (var i = 0; i < n && i < b.length; i++) out += ('0' + b[i].toString(16)).slice(-2);
    return out;
}
function ascii(b, n) {
    var out = '';
    for (var i = 0; i < n && i < b.length; i++) out += (b[i] > 31 && b[i] < 127) ? String.fromCharCode(b[i]) : '.';
    return out;
}

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500 && c++ < 200) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    var magic = String.fromCharCode.apply(null, h);
                    if (magic === 'X1V5fzTo') {
                        var n = this.n, src = this.src, dst = this.dst;
                        console.log('HIT n=' + n + ' src=' + src + ' dst=' + dst);
                        // 同步读 src 密文头
                        var sb = Array.prototype.slice.call(new Uint8Array(src.readByteArray(Math.min(32, n))));
                        console.log('SRC: ' + hex(sb, 32));
                        // 同步读 dst (onLeave 后解密可能已完成 — 解密在拷贝后的调用链)
                        try {
                            var db = Array.prototype.slice.call(new Uint8Array(dst.readByteArray(Math.min(32, n))));
                            console.log('DST: ' + hex(db, 32) + ' "' + ascii(db, 16) + '"');
                        } catch (e) { console.log('DST: ERR'); }
                    }
                }
            } catch (e) {}
        }
    }
});
console.log('READY');
