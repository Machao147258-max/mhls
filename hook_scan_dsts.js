// 记录所有大拷贝的 dst, 5s 后读 (找解密明文 TSYS/luac 头)
var memcpy = Module.findGlobalExportByName('memcpy');
var c = 0;
var dsts = [];

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500 && c++ < 300) {
            dsts.push({ dst: this.dst, n: this.n });
        }
    }
});

// 20s 后统一读所有 dst (解密已完成)
setTimeout(function () {
    console.log('=== SCAN ' + dsts.length + ' dsts');
    dsts.forEach(function (d) {
        try {
            var b = Array.prototype.slice.call(new Uint8Array(d.dst.readByteArray(8)));
            var h = '';
            for (var i = 0; i < b.length; i++) h += ('0' + b[i].toString(16)).slice(-2);
            var as = String.fromCharCode.apply(null, b);
            // 找明文特征: 1bLua / TSYS / 非X1V5
            if (b[0] === 0x1b || h.indexOf('54535953') === 0 || (as.indexOf('X1V5') !== 0 && b[0] !== 0x00 && b[0] !== 0xff)) {
                console.log('PLAIN? n=' + d.n + ' dst=' + d.dst + ' ' + h + ' "' + as.slice(0, 8) + '"');
            }
        } catch (e) {}
    });
    console.log('=== DONE');
}, 20000);
console.log('READY-V3');
