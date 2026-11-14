// 多轮 dump 版: 捕获 X1V5fzTo 密文 → 每 60s 重读所有 hits, 解密完成即存明文到 /data/local/tmp/
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
        if (this.n > 500 && c++ < 2000) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    var magic = String.fromCharCode.apply(null, h);
                    if (magic === 'X1V5fzTo') {
                        console.log('HIT n=' + this.n + ' src=' + this.src + ' dst=' + this.dst);
                        hits.push({ dst: this.dst, n: this.n, saved: false });
                    }
                }
            } catch (e) {}
        }
    }
});

function dumpPlain(round) {
    console.log('=== ROUND ' + round + ': ' + hits.length + ' hits');
    var saved = 0;
    hits.forEach(function (x, i) {
        if (x.saved) return;
        try {
            var b = x.dst.readByteArray(8);
            if (b) {
                var arr = Array.prototype.slice.call(new Uint8Array(b));
                var hex = '';
                for (var j = 0; j < arr.length; j++) hex += ('0' + arr[j].toString(16)).slice(-2);
                // 明文特征: 非 X1V5fzTo 头
                if (hex.indexOf('58315635667a546f') !== 0 && arr[0] !== 0x00 && arr[0] !== 0xff) {
                    var full = x.dst.readByteArray(x.n);
                    if (full) {
                        var f = '/data/local/tmp/tom_plain_' + i + '_' + x.n + '_r' + round + '.bin';
                        try {
                            var w = new File(f, 'w');
                            w.write(full);
                            w.close();
                            console.log('  ★SAVED[' + i + '] n=' + x.n + ' head=' + hex + ' -> ' + f);
                            x.saved = true;
                            saved++;
                        } catch (e) { console.log('  save fail: ' + e); }
                    }
                }
            }
        } catch (e) {}
    });
    console.log('=== ROUND ' + round + ' DONE saved=' + saved);
}

// 每 60s dump 一轮, 跑 10 轮
var round = 0;
setInterval(function () {
    round++;
    dumpPlain(round);
}, 60000);
console.log('READY-MULTI');
