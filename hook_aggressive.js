// 激进版: 捕获 X1V5fzTo 密文 → 15s 后扫描所有记录缓冲找明文 (luac/TSYS)
var memcpy = Module.findGlobalExportByName('memcpy');
var c = 0;
var bufs = [];
var hits = [];

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500 && c++ < 500) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    var magic = String.fromCharCode.apply(null, h);
                    if (magic === 'X1V5fzTo') {
                        console.log('HIT n=' + this.n + ' src=' + this.src + ' dst=' + this.dst);
                        hits.push({ src: this.src, dst: this.dst, n: this.n });
                    } else {
                        bufs.push({ p: this.dst, n: this.n });
                    }
                }
            } catch (e) {}
        }
    }
});

setTimeout(function () {
    console.log('=== SCAN: ' + hits.length + ' hits, ' + bufs.length + ' bufs');
    // 1) 重新读 hit 的 dst (解密后)
    hits.forEach(function (x) {
        try {
            var b = Array.prototype.slice.call(new Uint8Array(x.dst.readByteArray(8)));
            var hx = '';
            for (var i = 0; i < b.length; i++) hx += ('0' + b[i].toString(16)).slice(-2);
            var as = String.fromCharCode.apply(null, b);
            console.log('HITDST n=' + x.n + ' ' + hx + ' "' + as.slice(0, 4) + '"');
        } catch (e) {}
    });
    // 2) 扫描所有大缓冲 (找 1bLua / TSYS / 明文)
    var found = 0;
    bufs.forEach(function (b) {
        if (found > 30) return;
        try {
            var b0 = Array.prototype.slice.call(new Uint8Array(b.p.readByteArray(8)));
            var hx = '';
            for (var i = 0; i < b0.length; i++) hx += ('0' + b0[i].toString(16)).slice(-2);
            if (b0[0] === 0x1b && b0[1] === 0x4c) {  // 0x1bLua
                console.log('★★LUAC n=' + b.n + ' @' + b.p + ' ' + hx);
                found++;
            } else if (hx.indexOf('54535953') === 0) {  // TSYS
                console.log('★TSYS n=' + b.n + ' @' + b.p + ' ' + hx);
                found++;
            }
        } catch (e) {}
    });
    console.log('=== DONE found=' + found);
}, 15000);
console.log('READY-AGGRESSIVE');
