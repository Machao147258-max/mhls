// hook_onetime.js — 一次性 DELTA hook: 首次触发打印寄存器+key, 立即 detach (不卡游戏)
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'a');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] 一次性脚本 ' + Date.now());
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
                    (function (addr) {
                        try {
                            Interceptor.attach(addr, {
                                onEnter: function () {
                                    // 首次触发: 打印 + detach 自己
                                    try {
                                        Interceptor.detach(addr);
                                    } catch (e) {}
                                    try {
                                        var ctx = this.context;
                                        L('[★D] ' + addr + ' rsi=' + ctx.rsi + ' rdx=' + ctx.rdx + ' r14=' + ctx.r14 + ' rcx=' + ctx.rcx);
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
                    })(hits[hi].address);
                }
            } catch (e) {}
        }
        L('[+] ONETIME hooks: ' + total);
        clearInterval(iv);
    } catch (e) {
        if (tries % 5 === 0) L('[err] ' + e);
    }
}, 800);
