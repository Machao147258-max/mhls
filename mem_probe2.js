// mem_probe2.js — 扩大词表: 经济/玩家/会话数据内存驻留
var LF = '/data/data/com.netease.tom/files/mem2.txt';
var f = new File(LF, 'a');
function L(s) { try { f.write(s + '\n'); f.flush(); } catch (e) {} }
L('[+] mem2 ' + Date.now());

var needles = [
    ['gold', 'gold'],
    ['diamond', 'diamond'],
    ['coin', 'coin'],
    ['money', 'money'],
    ['reward', 'reward'],
    ['vip', 'vip'],
    ['level', 'level'],
    ['exp', 'exp'],
    ['token', 'token'],
    ['session', 'session'],
    ['ticket', 'ticket'],
    ['item', 'itemid'],
    ['role_name', 'xindagag'],
    ['battle', 'battle_id'],
    ['udid', 'be1c235ad80959f7'],
    ['key64', '1a911bcd81073eaea0760e9356ef10ef'],
    ['key642', '57e66e8f6798ae97d3b44718325e5557'],
];
var found = [];
var ranges = Process.enumerateRanges('rw-');
var scanned = 0;
ranges.forEach(function (r) {
    if (r.size > 64 * 1024 * 1024) return;
    if (r.size < 4096) return;
    scanned++;
    try {
        needles.forEach(function (n) {
            try {
                var res = Memory.scanSync(r.base, r.size, n[1]);
                if (res.length) {
                    found.push([n[0], res[0].address]);
                    L('[HIT] ' + n[0] + ' x' + res.length + ' @ ' + res[0].address);
                }
            } catch (e) {}
        });
    } catch (e) {}
});
L('[+] scanned=' + scanned + ' hit_types=' + found.length);
found.forEach(function (p) {
    try {
        var a = p[1];
        var bytes = new Uint8Array(a.sub(128).readByteArray(512));
        var s = '';
        for (var i = 0; i < bytes.length; i++) {
            var c = bytes[i];
            s += (c >= 32 && c < 127) ? String.fromCharCode(c) : '.';
        }
        L('[CTX:' + p[0] + '] ' + s);
    } catch (e) {}
});
L('[+] done');