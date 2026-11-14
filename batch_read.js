// 批量读 60 个 src 地址头 16B, 找已解密 (非 X1V5 头)
var addrs = "72b5cb1ef83c 72b5cb1ee0bc 72b5cb1ec61c 72b5cb1e3598 72b5cb4b7150 72b5cb4c068c 72b5cb4c2ce8 72b5cc9de47c 72b5cc9e5380 72b5cf9e15f8 72b5cf9e1abc 72b5cfb3bbb4 72b5cfbf9030 72b5cfbf9ac0 72b5cfd0e458 72b5cfd0f82c 72b5cfd19c3c 72b5cfeb9c1c 72b5d03d5850 72b5d04be13c 72b5d04bf920 72b5d04c03dc 72b5d04c29d4 72b5d04c30c0 72b5d04c36f0 72b5d04c46e0 72b5d04c4d08 72b5d06ee23c 72b5d06ef00c 72b5d06f1584 72b5d06f2924 72b5d06f2f24 72b5d06f3134 72b5d06f7178 72b5d06f78d4 72b5d06f7980 72b5d06f92b8 72b5d06f9bd4 72b5d06fa8d4 72b5d06fabdc 72b5d06fae70 72b5d06fafc4 72b5d06fb07c 72b5d06fb7e4 72b5d06fb89c 72b5d06fbcec 72b5d06fbfa8 72b5e6daf074 72b5e6daf1b0 72b5e6daf3a0 72b5e6dafb40 72b5e6dafc40 72b5e6dafc5c 72b5e6daff2c 72b5e6daff60 72b5e6dafff4 72b5ec3c0a2c 72b5ec3c1298 72b5ec3c1440 72b5ec3c3134 72b5ec3c3e88 72b5ec3c43ec".split(' ');
addrs.forEach(function (a) {
    try {
        var b = Array.prototype.slice.call(new Uint8Array(ptr('0x' + a).readByteArray(16)));
        var h = '';
        for (var i = 0; i < b.length; i++) h += ('0' + b[i].toString(16)).slice(-2);
        var isCipher = (b[0] === 0x58 && b[1] === 0x31 && b[2] === 0x56 && b[3] === 0x35);
        if (!isCipher && b[0] !== 0x00) {
            console.log('★PLAIN ' + a + ': ' + h);
        } else if (b[0] !== 0x00) {
            console.log('cipher ' + a + ': ' + h.slice(0, 16));
        }
    } catch (e) {}
});
console.log('BATCH-DONE');