// 读 multi.log 捕获的关键 src/dst (加载完成后可能已是明文)
var pts = [
    ['0x72b5cb1ef83c', 277740],   // 27万字节大脚本 src (max)
    ['0x72b5cac04300', 277740],   // 对应 dst
    ['0x72b5d06f92b8', 41912],    // 41912 大脚本 src
    ['0x72b337a280f0', 41912],    // 对应 dst
    ['0x72b5e6dafc5c', 28232],    // 28232 src
    ['0x72b477a5c780', 28232],    // dst
    ['0x72b5ec3c1298', 18008],
    ['0x72b42795d860', 18008]
];
pts.forEach(function (p) {
    try {
        var b = Array.prototype.slice.call(new Uint8Array(ptr(p[0]).readByteArray(16)));
        var h = '';
        for (var i = 0; i < b.length; i++) h += ('0' + b[i].toString(16)).slice(-2);
        var as = b.map(function (x) { return (x > 31 && x < 127) ? String.fromCharCode(x) : '.'; }).join('');
        var plain = (h.indexOf('58315635667a546f') !== 0) ? '★PLAIN?' : 'cipher';
        console.log(p[0] + ' n=' + p[1] + ' ' + plain + ' ' + h + ' "' + as.slice(0, 8) + '"');
    } catch (e) { console.log(p[0] + ': ERR'); }
});