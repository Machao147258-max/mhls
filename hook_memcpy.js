// Hook memcpy/memmove: 抓大块内存拷贝 (解密输出/脚本加载必经)
// 过滤 > 1000 字节的拷贝, 打印 src/dst/大小
var memcpy = Module.findGlobalExportByName('memcpy');
var memmove = Module.findGlobalExportByName('memmove');
var c = 0;

function hookMem(fn, name) {
    if (!fn) { console.log('[mem] no ' + name); return; }
    Interceptor.attach(fn, {
        onEnter: function (args) {
            this.dst = args[0];
            this.src = args[1];
            this.n = args[2].toInt32();
            this.t = Date.now();
        },
        onLeave: function (ret) {
            if (this.n > 500 && c++ < 200) {
                console.log('[' + name + '] n=' + this.n + ' src=' + this.src + ' dst=' + this.dst + ' t=' + this.t);
                // 尝试 dump 前 32 字节 (密文/明文特征)
                try {
                    var b = this.src.readByteArray(Math.min(32, this.n));
                    if (b) {
                        var bytes = Array.prototype.slice.call(new Uint8Array(b));
                        var hex = bytes.map(function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
                        var ascii = bytes.map(function (x) { return (x > 31 && x < 127) ? String.fromCharCode(x) : '.'; }).join('');
                        console.log('    src32: ' + hex + '  "' + ascii + '"');
                    }
                } catch (e) {}
            }
        }
    });
    console.log('[mem] ' + name + ' hooked');
}

hookMem(memcpy, 'memcpy');
hookMem(memmove, 'memmove');
console.log('[mem] ready');
