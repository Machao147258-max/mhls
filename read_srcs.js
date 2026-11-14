// 读已知 src 地址 (若解密原地, src 已变明文 luac)
var addrs = [
    '0x72b5cfc9fdf8',  // 39808B 密文 src
    '0x72b5ec09c9e0',  // 1688B
    '0x72b5ec09c110',  // 6800B
    '0x72b5ec09c0cc',  // 4500B
    '0x72b5ec09c2f8'   // 5620B
];
addrs.forEach(function (a) {
    try {
        var b = Array.prototype.slice.call(new Uint8Array(ptr(a).readByteArray(16)));
        var h = '';
        for (var i = 0; i < b.length; i++) h += ('0' + b[i].toString(16)).slice(-2);
        var as = b.map(function (x) { return (x > 31 && x < 127) ? String.fromCharCode(x) : '.'; }).join('');
        console.log(a + ': ' + h + ' "' + as.slice(0, 8) + '"');
    } catch (e) { console.log(a + ': ERR'); }
});
