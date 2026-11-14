// hook_boot2.js — 启动解密窗口 hook: DELTA 一次性 + recv + open 追踪
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'a');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] boot2 ' + Date.now());
function hex(b) {
    var u = new Uint8Array(b);
    var s = "";
    for (var i = 0; i < u.length; i++) s += ("0" + u[i].toString(16)).slice(-2);
    return s;
}
function toStr(b) {
    var u = new Uint8Array(b);
    var s = "";
    for (var i = 0; i < u.length; i++) {
        var c = u[i];
        s += (c >= 32 && c < 127) ? String.fromCharCode(c) : ".";
    }
    return s;
}
// 防自杀 (幂等)
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        try {
            Interceptor.replace(p, new NativeCallback(function () { return 0; }, 'int', ['int']));
        } catch (e) {}
    } catch (e) {}
});
// recv 追踪
try {
    var rp = Module.getGlobalExportByName('recv');
    Interceptor.attach(rp, {
        onEnter: function (a) { this.b = a[1]; this.n = a[2].toInt32(); },
        onLeave: function (r) {
            var n = r.toInt32();
            if (n > 8 && n < 65536) {
                try {
                    var raw = this.b.readByteArray(Math.min(n, 16));
                    var hx = hex(raw);
                    L('[RECV] len=' + n + ' head=' + hx);
                } catch (e) {}
            }
        }
    });
} catch (e) {}
// DELTA 一次性 + 周边函数
var tries = 0;
var iv = setInterval(function () {
    tries++;
    try {
        var ranges = Process.enumerateRanges('rwx');
        var total = 0;
        for (var ri = 0; ri < ranges.length; ri++) {
            var r = ranges[ri];
            if (r.size > 0x30000000) continue;
            var hits = [];
            try { hits = Memory.scanSync(r.base, r.size, 'b9 79 37 9e'); } catch (e) {}
            for (var hi = 0; hi < hits.length; hi++) {
                (function (dAddr) {
                    try {
                        Interceptor.attach(dAddr, {
                            onEnter: function () {
                                try { Interceptor.detach(dAddr); } catch (e) {}
                                try {
                                    var ctx = this.context;
                                    L('[★D] ' + dAddr + ' rsi=' + ctx.rsi + ' rdx=' + ctx.rdx + ' r14=' + ctx.r14);
                                    ['rsi', 'rdx', 'rcx', 'r14', 'r8', 'r9'].forEach(function (rn) {
                                        try {
                                            var p = ctx[rn];
                                            if (p && !p.isNull()) {
                                                var kb = p.readByteArray(16);
                                                var s = toStr(kb);
                                                var pr = 0;
                                                for (var i = 0; i < 16; i++) if (s.charCodeAt(i) !== 46) pr++;
                                                if (pr >= 4 || kb[0] === 0x1b) {
                                                    L('[★K ' + rn + '] ' + JSON.stringify(s) + ' hex=' + hex(kb));
                                                }
                                            }
                                        } catch (e) {}
                                    });
                                } catch (e) {}
                            }
                        });
                        total++;
                    } catch (e) {}
                    // 也 hook DELTA 往前最近的函数入口
                    try {
                        var zone = dAddr.sub(0x2000);
                        var ents = Memory.scanSync(zone, 0x2000, '55 48 89 e5');
                        for (var ei = 0; ei < ents.length; ei++) {
                            (function (fnAddr) {
                                try {
                                    Interceptor.attach(fnAddr, {
                                        onEnter: function () {
                                            try { Interceptor.detach(fnAddr); } catch (e) {}
                                            try {
                                                var ctx = this.context;
                                                L('[★FN] ' + fnAddr + ' rsi=' + ctx.rsi + ' rdx=' + ctx.rdx + ' r14=' + ctx.r14);
                                            } catch (e) {}
                                        }
                                    });
                                    total++;
                                } catch (e) {}
                            })(ents[ei].address);
                        }
                    } catch (e) {}
                })(hits[hi].address);
            }
        }
        L('[+] BOOT2 hooks: ' + total);
        clearInterval(iv);
    } catch (e) {
        if (tries % 5 === 0) L('[err] ' + e);
    }
}, 800);
