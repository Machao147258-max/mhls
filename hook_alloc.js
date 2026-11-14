// hook malloc: 捕获解密输出缓冲分配 (解密函数输出=新分配的大块)
// 输出缓冲特征: 分配后不久写入非密文数据
var malloc = Module.findGlobalExportByName('malloc');
var calloc = Module.findGlobalExportByName('calloc');
var c = 0;

function hookAlloc(fn, name) {
    if (!fn) return;
    Interceptor.attach(fn, {
        onEnter: function (args) {
            this.sz = name === 'malloc' ? args[0].toInt32() : (args[0].toInt32() * args[1].toInt32());
        },
        onLeave: function (ret) {
            var sz = this.sz;
            if (sz > 1000 && sz < 2000000 && c++ < 80) {
                console.log('ALLOC ' + name + ' n=' + sz + ' ptr=' + ret);
            }
        }
    });
}
hookAlloc(malloc, 'malloc');
hookAlloc(calloc, 'calloc');
console.log('READY-ALLOC');
