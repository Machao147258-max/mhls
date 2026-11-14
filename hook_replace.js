// hook_replace.js — replace 解密入口, 让 houdini 重转译执行我们的代码, 抓 key
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
var done = false;
var tries = 0;
var iv = setInterval(function () {
    if (done) return;
    tries++;
    try {
        var p = ptr('0x400020e85261c'); // 文件映射的 ARM64 解密入口
        p.readU32();
        done = true;
        clearInterval(iv);
        L('[+] 就绪 第' + tries + '次, replace 解密入口...');
        var keyLog = new NativeCallback(function (x0, x1, x2, x3) {
            try {
                var kb = ptr(x2).readByteArray(16);
                L('[★REPLACE-decwrap] data=' + x0 + ' len=' + x1 + ' key=' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb));
            } catch (e) {
                L('[★REPLACE] x0=' + x0 + ' x1=' + x1 + ' x2=' + x2 + ' x3=' + x3 + ' err=' + e);
            }
            return 0;
        }, 'pointer', ['pointer', 'int', 'pointer', 'pointer']);
        Interceptor.replace(p, keyLog);
        L('[+] replace OK @' + p);
        // 也 replace reader
        try {
            var rp = ptr('0x400020e85548');
            Interceptor.replace(rp, new NativeCallback(function (x0, x1, x2, x3) {
                if (x1 === 16) {
                    try {
                        var kb = ptr(x0).readByteArray(16);
                        L('[★REPLACE-reader16] ' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb));
                    } catch (e) {}
                }
                return ptr(0);
            }, 'pointer', ['pointer', 'int', 'int', 'pointer']));
            L('[+] replace reader OK');
        } catch (e) { L('[-] reader: ' + e); }
        L('[+] 等待调用...');
    } catch (e) {
        if (tries > 500) { clearInterval(iv); L('[-] 100s 未就绪'); }
    }
}, 200);
