// 静默版: hook 捕获 X1V5fzTo 密文 → 每 60s 静默 dump 解密明文到 /data/local/tmp/
// 关键: 不打印 HIT (防 frida 输出洪峰崩溃), 只打印保存成功
var memcpy = Module.findGlobalExportByName('memcpy');
var hits = [];
var n = 0;

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    if (h[0] === 0x58 && h[1] === 0x31 && h[2] === 0x56 && h[3] === 0x35) {  // X1V5
                        hits.push({ dst: this.dst, n: this.n, saved: false });
                    }
                }
            } catch (e) {}
        }
    }
});

function dumpPlain(round) {
    var saved = 0;
    hits.forEach(function (x) {
        if (x.saved) return;
        try {
            var b = x.dst.readByteArray(8);
            if (b) {
                var arr = Array.prototype.slice.call(new Uint8Array(b));
                // 明文特征: 头不是 X1V5fzTo (X=0x58,1=0x31,5=0x56,V=0x35) 
                var isCipher = (arr[0] === 0x58 && arr[1] === 0x31 && arr[2] === 0x56 && arr[3] === 0x35);
                if (!isCipher && arr[0] !== 0x00 && arr[0] !== 0xff) {
                    var full = x.dst.readByteArray(x.n);
                    if (full) {
                        var f = '/data/local/tmp/tp_' + round + '_' + x.n + '_' + hits.indexOf(x) + '.bin';
                        var w = new File(f, 'w');
                        w.write(full);
                        w.close();
                        x.saved = true;
                        saved++;
                    }
                }
            }
        } catch (e) {}
    });
    if (saved > 0) console.log('R' + round + ' saved=' + saved + ' total=' + hits.length);
}

var round = 0;
setInterval(function () {
    round++;
    dumpPlain(round);
}, 60000);
console.log('OK-SILENT');