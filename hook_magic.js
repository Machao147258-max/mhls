// 增强版: 捕获 X1V5fzTo 密文完整内容 + 解密后的明文 (dump 到 console)
var memcpy = Module.findGlobalExportByName('memcpy');
var c = 0;

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500 && c++ < 100) {
            try {
                var head = this.src.readByteArray(Math.min(12, this.n));
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    var magic = String.fromCharCode.apply(null, h.slice(0, 8));
                    if (magic === 'X1V5fzTo') {
                        console.log('★★★★★ X1V5fzTo COPY n=' + this.n + ' src=' + this.src + ' dst=' + this.dst);
                        // dump 完整密文前 64B
                        var b = this.src.readByteArray(Math.min(64, this.n));
                        var bytes = Array.prototype.slice.call(new Uint8Array(b));
                        var hex = bytes.map(function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
                        console.log('  SRC64: ' + hex);
                        // 解密后 dst 内容 (延迟 1ms 让解密写)
                        setTimeout(function () {
                            try {
                                var db = this.dst.readByteArray(Math.min(64, this.n));
                                if (db) {
                                    var db2 = Array.prototype.slice.call(new Uint8Array(db));
                                    var dh = db2.map(function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
                                    var ascii = db2.map(function (x) { return (x > 31 && x < 127) ? String.fromCharCode(x) : '.'; }).join('');
                                    console.log('  DST64: ' + dh + ' "' + ascii + '"');
                                }
                            } catch (e) { console.log('  dst read fail'); }
                        }.bind(this), 50);
                    }
                }
            } catch (e) {}
        }
    }
});
console.log('[v2] ready');
