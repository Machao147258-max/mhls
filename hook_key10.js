// hook_key10.js — spawn 早期: patch 自杀函数(ret) + hook 解密, 文件日志
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'w');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] 脚本启动 ' + Date.now());
var BASE = ptr('0x400020e00000');
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

// 防自杀: replace libc 自杀函数为空操作
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        if (!p) {
            L('[-] replace ' + n + ': 无导出');
            return;
        }
        Interceptor.replace(p, new NativeCallback(function () {
            L('[防自杀] ' + n + ' 被调用!');
            return 0;
        }, 'int', ['int']));
        L('[+] 防自杀 ' + n + ' @' + p);
    } catch (e) {
        L('[-] replace ' + n + ' 失败: ' + e);
    }
});

var targets = {
    'decwrap': 0x85261c, 'stream': 0x8ab25c,
    'blk108': 0x8ab108, 'blk14f4': 0x8b14f4, 'luadec': 0x4095b0,
    'luaenc': 0x408ddc, 'encxt': 0x3fc774, 'encwrap': 0x8529cc
};
function makeHandler(k) {
    return {
        onEnter: function (args) {
            try {
                if (k === 'decwrap') {
                    var kb = args[2].readByteArray(16);
                    L('[★decwrap] key=' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb));
                } else if (k === 'stream' || k === 'blk108' || k === 'blk14f4') {
                    L('[' + k + '] x0=' + args[0] + ' x1=' + args[1] + ' x2=' + args[2]);
                } else {
                    L('[' + k + '] L=' + args[0]);
                }
            } catch (e) {
                L('[' + k + '] err ' + e);
            }
        }
    };
}
var done = false;
var tries = 0;
var iv = setInterval(function () {
    if (done) return;
    tries++;
    if (tries % 10 === 0) L('[tick] ' + tries);
    try {
        Interceptor.attach(BASE.add(0x852548), function () {});
        done = true;
        clearInterval(iv);
        L('[+] so 就绪 第' + tries + '次, 装 hook...');
        Object.keys(targets).forEach(function (k) {
            try {
                Interceptor.attach(BASE.add(targets[k]), makeHandler(k));
                L('[+] hook ' + k + ' OK');
            } catch (e) {
                L('[-] hook ' + k + ' 失败: ' + e);
            }
        });
        L('[+] 全部就绪, 等待解密...');
    } catch (e) {
        if (tries > 500) {
            clearInterval(iv);
            L('[-] so 100s 未就绪');
        }
    }
}, 200);
