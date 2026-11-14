// 游戏进程内 dump 明文到 app 私有目录 (frida agent 有 app 权限)
var targets = [
    [ptr('0x72b5cf9e15f8'), 248396, 's1.bin'],
    [ptr('0x72b5cf9e1abc'), 249412, 's2.bin'],
    [ptr('0x72b5cfeb9c1c'), 154636, 's3.bin'],
    [ptr('0x72b5d04c29d4'), 123920, 's4.bin'],
    [ptr('0x72b5d04c30c0'), 119116, 's5.bin'],
    [ptr('0x72b5d04c46e0'), 113964, 's6.bin'],
    [ptr('0x72b5d04c4d08'), 114028, 's7.bin']
];
var dir = '/data/user/0/com.netease.tom/files/dump';
try {
    var d = new File(dir, 'w'); d.close();  // 测试可写
    console.log('DIR WRITABLE');
} catch (e) {
    console.log('DIR FAIL: ' + e);
    dir = '/data/local/tmp';
}
targets.forEach(function (t) {
    try {
        var b = t[0].readByteArray(t[1]);
        if (b) {
            var f = new File(dir + '/' + t[2], 'w');
            f.write(b);
            f.close();
            console.log('SAVED ' + t[2] + ' n=' + t[1] + ' head=' + b[0].toString(16));
        } else {
            console.log('READ FAIL ' + t[2]);
        }
    } catch (e) {
        console.log('FAIL ' + t[2] + ': ' + e);
    }
});
console.log('ALL DONE');