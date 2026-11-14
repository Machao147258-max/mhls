// 终极版: 捕获 X1V5fzTo 密文 → 60s 后 dump 所有 dst 完整内容到设备文件
// 解密后的 dst = 明文 luac (X1V5fzTo 头会被解密覆盖)
var memcpy = Module.findGlobalExportByName('memcpy');
var c = 0;
var hits = [];

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500 && c++ < 1000) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    var magic = String.fromCharCode.apply(null, h);
                    if (magic === 'X1V5fzTo') {
                        console.log('HIT n=' + this.n + ' src=' + this.src + ' dst=' + this.dst);
                        hits.push({ dst: this.dst, n: this.n });
                    }
                }
            } catch (e) {}
        }
    }
});

setTimeout(function () {
    console.log('=== DUMPING ' + hits.length + ' hits');
    var fs = require('fs');
    hits.forEach(function (x, i) {
        try {
            var b = x.dst.readByteArray(x.n);
            if (b) {
                var arr = Array.prototype.slice.call(new Uint8Array(b));
                var hex = '';
                for (var j = 0; j < 16 && j < arr.length; j++) hex += ('0' + arr[j].toString(16)).slice(-2);
                // 判断是否已解密 (头非 X1V5fzTo)
                var isPlain = (hex.indexOf('58315635667a546f') !== 0);
                console.log('DUMP[' + i + '] n=' + x.n + ' head=' + hex + ' plain=' + isPlain);
                if (isPlain) {
                    var f = '/data/local/tmp/tom_plain_' + i + '_' + x.n + '.bin';
                    try {
                        var w = new File(f, 'w');
                        w.write(b);
                        w.close();
                        console.log('  SAVED ' + f);
                    } catch (e) { console.log('  save fail: ' + e); }
                }
            }
        } catch (e) { console.log('  read fail: ' + e); }
    });
    console.log('=== DONE');
}, 60000);
console.log('READY-FINAL');
