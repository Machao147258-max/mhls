// hook_trace.js — hook 文件读取 + 解密, 打印调用栈溯源
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
    try {
        return Thread.backtrace(this.context, Backtracer.ACCURATE).slice(0, 10).map(function (a) {
            return a.toString();
        }).join(' <- ');
    } catch (e) {
        return 'bt err';
    }
}
// hook libc 文件读取
['open', 'fopen', 'read', 'fread', 'fgets'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onEnter: function (args) {
                try {
                    var s = args[0].readCString();
                    if (s && (s.indexOf('hotfix') >= 0 || s.indexOf('filelist') >= 0 || s.indexOf('launcher') >= 0 || s.indexOf('.bin') >= 0 || s.indexOf('lua') >= 0 || s.indexOf('src') >= 0)) {
                        console.log('[FILE:' + n + '] ' + s + '  <<< ' + bt());
                    }
                } catch (e) {}
            }
        });
        console.log('[+] 文件 hook ' + n + ' OK');
    } catch (e) {
        console.log('[-] 文件 hook ' + n + ': ' + e);
    }
});
// hook 解密函数
[['decwrap', 0x85261c], ['reader', 0x852548], ['stream', 0x8ab25c]].forEach(function (t) {
    try {
        Interceptor.attach(BASE.add(t[1]), {
            onEnter: function (args) {
                try {
                    if (t[0] === 'decwrap') {
                        var kb = args[2].readByteArray(16);
                        console.log('[★decwrap] key=' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb) + ' <<< ' + bt());
                    } else if (t[0] === 'reader') {
                        console.log('[reader] len=' + args[1].toInt32() + ' <<< ' + bt());
                    } else {
                        console.log('[' + t[0] + '] x0=' + args[0] + ' <<< ' + bt());
                    }
                } catch (e) {
                    console.log('[' + t[0] + '] err ' + e);
                }
            }
        });
        console.log('[+] 解密 hook ' + t[0] + ' OK');
    } catch (e) {
        console.log('[-] 解密 hook ' + t[0] + ': ' + e);
    }
});
console.log('[+] 全部就绪');
