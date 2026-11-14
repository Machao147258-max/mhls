// 读之前捕获的 dst 地址 (解密后应为明文 luac)
var addrs = [
    '0x72b497a3ce80', '0x72b3d79da3c0', '0x72b528b392f0', '0x72b337f78640',
    '0x72b4d79f0340', '0x72b5ec09c9e0'
];
addrs.forEach(function (a) {
    try {
        var p = ptr(a);
        var b = Array.prototype.slice.call(new Uint8Array(p.readByteArray(16)));
        var h = '';
        for (var i = 0; i < b.length; i++) h += ('0' + b[i].toString(16)).slice(-2);
        console.log(a + ': ' + h);
    } catch (e) { console.log(a + ': ERR'); }
});
