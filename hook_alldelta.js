// hook_alldelta.js — 扫所有 rwx 段 DELTA 全 hook, 抓 key (纯观察)
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'a');
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
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.replace(p, new NativeCallback(function () {
            L('[防自杀] ' + n);
            return 0;
        }, 'int', ['int']));
        L('[+] 防自杀 ' + n);
    } catch (e) { L('[-] ' + n + ': ' + e); }
});
function dump(tag, ctx) {
    try {
        var regs = ['rsi', 'rdx', 'rcx', 'r8', 'r9', 'r14', 'r15', 'rdi', 'rbx'];
        var line = '[REG ' + tag + ']';
        for (var i = 0; i < regs.length; i++) {
            try { line += ' ' + regs[i] + '=' + ctx[regs[i]]; } catch (e) {}
        }
        L(line);
        regs.forEach(function (rn) {
            try {
                var p = ctx[rn];
                if (p && !p.isNull()) {
                    var kb = p.readByteArray(16);
                    var s = toStr(kb);
                    var pr = 0;
                    for (var i = 0; i < 16; i++) if (s.charCodeAt(i) !== 46) pr++;
                    if (pr >= 4 || kb[0] === 0x1b) {
                        L('[★MEM ' + rn + '@' + tag + '] ' + JSON.stringify(s) + ' hex=' + hex(kb));
                    }
                }
            } catch (e) {}
        });
    } catch (e) { L('[dump err] ' + e); }
}
var tries = 0;
var iv = setInterval(function () {
    tries++;
    try {
        var ranges = Process.enumerateRanges('rwx');
        var total = 0;
        for (var ri = 0; ri < ranges.length; ri++) {
            var r = ranges[ri];
            if (r.size > 0x30000000) continue;
            try {
                var hits = Memory.scanSync(r.base, r.size, 'b9 79 37 9e');
                for (var hi = 0; hi < hits.length; hi++) {
                    try {
                        Interceptor.attach(hits[hi].address, {
                            onEnter: function () { dump('D', this.context); }
                        });
                        total++;
                    } catch (e) {}
                }
            } catch (e) {}
        }
        L('[+] DELTA hooks: ' + total);
        L('[+] 全部就绪, 等待解密...');
        clearInterval(iv);
    } catch (e) {
        if (tries % 5 === 0) L('[err] ' + e);
    }
}, 1000);
