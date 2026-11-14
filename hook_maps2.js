// hook_maps2.js — 稳定 attach 版: 正确 rwxp 地址 hook + 点击触发
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'w');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] 脚本启动 ' + Date.now());
function hex(b) {
    var s = "";
    for (var i = 0; i < b.length; i++) s += ("0" + b[i].toString(16)).slice(-2);
    return s;
}
function toStr(b) {
    var s = "";
    for (var i = 0; i < b.length; i++) {
        var c = b[i];
        s += (c >= 32 && c < 127) ? String.fromCharCode(c) : ".";
    }
    return s;
}
var targets = {
    'decwrap': ptr('0x40002165261c'),
    'stream': ptr('0x4000216ab25c'),
    'blk108': ptr('0x4000216ab108'),
    'blk14f4': ptr('0x4000216b14f4'),
    'encwrap': ptr('0x4000216529cc')
};
Object.keys(targets).forEach(function (k) {
    try {
        Interceptor.attach(targets[k], {
            onEnter: function (args) {
                try {
                    if (k === 'decwrap') {
                        var kb = args[2].readByteArray(16);
                        L('[★decwrap] key=' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb));
                    } else {
                        L('[' + k + '] x0=' + args[0] + ' x1=' + args[1]);
                    }
                } catch (e) { L('[' + k + '] err ' + e); }
            }
        });
        L('[+] hook ' + k + ' OK');
    } catch (e) { L('[-] hook ' + k + ': ' + e); }
});
L('[+] 全部就绪');
