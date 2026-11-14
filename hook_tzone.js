// hook_tzone.js — 转译缓存 XXTEA 区全部函数入口 hook (一次性抓 key)
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'a');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] tzone 脚本 ' + Date.now());
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
            var hits = [];
            try { hits = Memory.scanSync(r.base, r.size, 'b9 79 37 9e'); } catch (e) {}
            if (hits.length === 0) continue;
            // 每个 DELTA: 往前 0x3000 找函数入口 (55 48 89 e5 / 48 83 ec / 55 41 57)
            for (var hi = 0; hi < hits.length; hi++) {
                var d = hits[hi].address;
                (function (dAddr) {
                    var zoneStart = dAddr.sub(0x3000);
                    var ents = [];
                    try { ents = Memory.scanSync(zoneStart, 0x3000, '55 48 89 e5'); } catch (e) {}
                    try { ents = ents.concat(Memory.scanSync(zoneStart, 0x3000, '48 83 ec')); } catch (e) {}
                    // hook 离 DELTA 最近的 3 个入口
                    var sorted = ents.map(function (e) { return e.address; })
                        .filter(function (a) { return a.compare(dAddr) < 0; })
                        .sort(function (a, b) { return b.compare(a); });
                    for (var ei = 0; ei < Math.min(3, sorted.length); ei++) {
                        (function (fnAddr) {
                            try {
                                Interceptor.attach(fnAddr, {
                                    onEnter: function () {
                                        try { Interceptor.detach(fnAddr); } catch (e) {}
                                        try {
                                            var ctx = this.context;
                                            L('[★FN] ' + fnAddr + ' (delta ' + dAddr + ')');
                                            L('[★REG] rsi=' + ctx.rsi + ' rdx=' + ctx.rdx + ' rcx=' + ctx.rcx + ' r8=' + ctx.r8 + ' r14=' + ctx.r14);
                                            ['rsi', 'rdx', 'rcx', 'r8', 'r9', 'r14', 'rdi', 'rbx'].forEach(function (rn) {
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
                                L('[+ fn hook @' + fnAddr + ']');
                            } catch (e) {}
                        })(sorted[ei]);
                    }
                })(d);
            }
            break; // 只处理第一个有 DELTA 的段
        }
        L('[+] TZONE hooks: ' + total);
        clearInterval(iv);
    } catch (e) {
        if (tries % 5 === 0) L('[err] ' + e);
    }
}, 800);
