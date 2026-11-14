// 捕获 X1V5fzTo + 延迟 5s 读 dst (解密完成后) — 单次 attach 内完成
var memcpy = Module.findGlobalExportByName('memcpy');
var c = 0;

function hex(b, n) {
    var out = '';
    for (var i = 0; i < n && i < b.length; i++) out += ('0' + b[i].toString(16)).slice(-2);
    return out;
}

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500 && c++ < 60) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    var magic = String.fromCharCode.apply(null, h);
                    if (magic === 'X1V5fzTo') {
                        var n = this.n, dst = this.dst;
                        console.log('HIT n=' + n + ' dst=' + dst);
                        // 5 秒后读 dst (解密完成)
                        var self = this;
                        setTimeout(function () {
                            try {
                                var b = Array.prototype.slice.call(new Uint8Array(dst.readByteArray(Math.min(32, n))));
                                var hexs = hex(b, 32);
                                var as = b.map(function (x) { return (x > 31 && x < 127) ? String.fromCharCode(x) : '.'; }).join('');
                                console.log('LATE-DST(' + n + '): ' + hexs + ' "' + as.slice(0, 16) + '"');
                            } catch (e) { console.log('LATE-ERR: ' + e); }
                        }, 5000);
                    }
                }
            } catch (e) {}
        }
    }
});
console.log('READY-V2');
