// hook_maps.js — 过滤 /proc/self/maps 隐藏 frida 特征 + 解密 hook + 防自杀
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
function bt() {
    try { return Thread.backtrace(this.context, Backtracer.ACCURATE).slice(0, 8).map(function (a) { return a.toString(); }).join('<-'); }
    catch (e) { return ''; }
}
// 防自杀
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.replace(p, new NativeCallback(function () {
            L('[防自杀] ' + n + bt());
            return 0;
        }, 'int', ['int']));
        L('[+] 防自杀 ' + n);
    } catch (e) { L('[-] ' + n + ': ' + e); }
});
// 过滤 maps: hook fgets (游戏读 maps 用 fgets/fread)
var inMaps = false;
['fgets', 'fread'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onEnter: function (args) {
                try {
                    var buf = n === 'fgets' ? args[0] : args[1];
                    var path = '';
                    if (n === 'fgets') {
                        // FILE* 无法直接读路径, 用 fd 检查
                        var fd = this.context.x19; // 猜
                    }
                } catch (e) {}
            },
            onLeave: function (retval) {
                try {
                    // 检查读取内容是否像 maps
                    var r = retval;
                    if (r.isNull()) return;
                    var buf = n === 'fgets' ? this.context.x0 : this.context.x1;
                    var s = buf.readCString();
                    if (s && s.indexOf('libcocos2dlua') >= 0 && s.indexOf('r--p') >= 0) {
                        inMaps = true;
                    }
                    if (inMaps && s) {
                        // 过滤: 隐藏 frida 段 (anonymous 且含 frida 特征)
                        if (s.indexOf('frida') >= 0 || s.indexOf('gum') >= 0 || (s.indexOf('00000000') >= 0 && s.indexOf('rw') >= 0 && s.indexOf('/') < 0)) {
                            L('[maps过滤] ' + s.trim().substring(0, 80));
                            r = ptr(0); // 返回空 = 结束读取
                        }
                    }
                    if (inMaps && s && s.indexOf('libcocos2dlua') < 0 && s.indexOf('r--p') < 0 && s.indexOf('rw-') < 0) {
                        inMaps = false;
                    }
                } catch (e) {}
            }
        });
        L('[+] maps hook ' + n);
    } catch (e) { L('[-] maps hook ' + n + ': ' + e); }
});
var done = false;
var tries = 0;
var iv = setInterval(function () {
    if (done) return;
    tries++;
    try {
        // 等 rwxp 段就绪: 0x400021652000 可读
        ptr('0x40002165261c').readU32();
        done = true;
        clearInterval(iv);
        L('[+] so 就绪 第' + tries + '次, 装解密 hook...');
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
                                L('[★decwrap] key=' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb) + ' bt=' + bt());
                            } else {
                                L('[' + k + '] x0=' + args[0] + ' x1=' + args[1] + ' bt=' + bt());
                            }
                        } catch (e) { L('[' + k + '] err ' + e); }
                    }
                });
                L('[+] hook ' + k + ' OK');
            } catch (e) { L('[-] hook ' + k + ': ' + e); }
        });
        L('[+] 全部就绪, 等待解密...');
    } catch (e) {
        if (tries > 500) { clearInterval(iv); L('[-] so 100s 未就绪'); }
    }
}, 200);
