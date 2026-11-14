// hook_net3.js — 网络包 + 文件 + 转译 DELTA 三合一 hook (轻量, 防抖)
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'a');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] net3 脚本 ' + Date.now());
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
// 防抖: 每地址只打一次
var fired = {};
function once(k, fn) {
    if (fired[k]) return;
    fired[k] = true;
    fn();
}
// 1. 网络包: recv/recvfrom + SSL_read
['recv', 'recvfrom'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onEnter: function (a) {
                this.buf = a[1];
                this.len = a[2].toInt32();
            },
            onLeave: function (ret) {
                var n = ret.toInt32();
                if (n > 0 && n <= 16384) {
                    try {
                        var raw = this.buf.readByteArray(Math.min(n, 64));
                        var s = toStr(raw);
                        // 找 X1V5fzTo 或高熵数据
                        var hx = hex(raw);
                        once('recv' + n, function () {
                            L('[RECV] len=' + n + ' head=' + hx.slice(0, 48) + ' str=' + JSON.stringify(s.slice(0, 32)));
                        });
                    } catch (e) {}
                }
            }
        });
        L('[+] recv hook');
    } catch (e) {}
});
['SSL_read', 'SSL_write'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onEnter: function (a) {
                this.buf = a[1];
                this.len = a[2].toInt32();
            },
            onLeave: function (ret) {
                var n = ret.toInt32();
                if (n > 0 && n <= 16384) {
                    try {
                        var raw = this.buf.readByteArray(Math.min(n, 64));
                        var hx = hex(raw);
                        once('ssl' + n, function () {
                            L('[SSL' + (n === 'SSL_write' ? 'W' : 'R') + '] len=' + n + ' head=' + hx.slice(0, 48));
                        });
                    } catch (e) {}
                }
            }
        });
        L('[+] ' + n + ' hook');
    } catch (e) {}
});
// 2. 文件: open/fopen 追踪
['open', 'openat', 'fopen'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onEnter: function (a) {
                try {
                    var path = (n === 'open') ? a[0].readCString() : (n === 'openat' ? a[1].readCString() : a[0].readCString());
                    if (path && (path.indexOf('hotfix') >= 0 || path.indexOf('.bin') >= 0 || path.indexOf('filelist') >= 0 || path.indexOf('download') >= 0 || path.indexOf('package') >= 0)) {
                        once('file' + path, function () {
                            L('[FILE] ' + path);
                        });
                    }
                } catch (e) {}
            }
        });
    } catch (e) {}
});
// 3. 转译 DELTA (一次性)
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
                                    try { Interceptor.detach(addr); } catch (e) {}
                                    try {
                                        var ctx = this.context;
                                        L('[★D] ' + addr + ' rsi=' + ctx.rsi + ' rdx=' + ctx.rdx + ' r14=' + ctx.r14);
                                        ['rsi', 'rdx', 'rcx', 'r14'].forEach(function (rn) {
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
        L('[+] NET3 就绪 (DELTA=' + total + ')');
        clearInterval(iv);
    } catch (e) {
        if (tries % 5 === 0) L('[err] ' + e);
    }
}, 800);
