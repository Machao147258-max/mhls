// hook_scan.js — spawn 早期: 防自杀 + 扫描 rwx 转译缓存找 XXTEA key 加载点 + hook
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
// 防自杀
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
// 扫描 rwx 段找 XXTEA (x86: DELTA 0x9e3779b9 = b9 79 37 9e)
function scanAndHook() {
    try {
        var ranges = Process.enumerateRanges('rwx');
        L('[+] rwx 段 ' + ranges.length + ' 个');
        for (var ri = 0; ri < ranges.length; ri++) {
            var r = ranges[ri];
            if (r.size > 0x20000000) continue;
            var found = false;
            Memory.scan(r.base, r.size, 'b9 79 37 9e', {
                onMatch: function (addr, size) {
                    if (!found) {
                        found = true;
                        L('[★DELTA] ' + addr + ' (base ' + r.base + ')');
                        // 在 DELTA 附近找 key 加载点: mov edx,[rsi] = 8b 16 / mov r11d,[r14+4] = 45 8b 5e 04
                        // 往 DELTA 前 0x3000 找 mov edx, dword ptr [rsi] (8b 16)
                        var zone = addr.sub(0x3000);
                        Memory.scan(zone, 0x3000, '8b 16', {
                            onMatch: function (a2) {
                                L('[★KEYLOAD] ' + a2);
                                Interceptor.attach(a2, {
                                    onEnter: function () {
                                        try {
                                            var kp = this.context.rsi;
                                            L('[★HIT] rsi=' + kp);
                                            if (kp && !kp.isNull()) {
                                                var kb = kp.readByteArray(16);
                                                L('[★★★KEY] ' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb));
                                            }
                                        } catch (e) { L('[hit err] ' + e); }
                                    }
                                });
                                L('[+] keyload hook @' + a2);
                            },
                            onComplete: function () {}
                        });
                        // 也找 mov r11d, dword ptr [r14+4] (45 8b 5e 04)
                        Memory.scan(zone, 0x3000, '45 8b 5e 04', {
                            onMatch: function (a3) {
                                L('[★KEYLOAD2] ' + a3);
                                Interceptor.attach(a3, {
                                    onEnter: function () {
                                        try {
                                            var kp = this.context.r14;
                                            L('[★HIT2] r14=' + kp);
                                            if (kp && !kp.isNull()) {
                                                var kb = kp.readByteArray(16);
                                                L('[★★★KEY] ' + JSON.stringify(toStr(kb)) + ' hex=' + hex(kb));
                                            }
                                        } catch (e) { L('[hit2 err] ' + e); }
                                    }
                                });
                                L('[+] keyload2 hook @' + a3);
                            },
                            onComplete: function () {}
                        });
                    }
                },
                onComplete: function () {}
            });
            if (found) return true;
        }
        return false;
    } catch (e) {
        L('[scan err] ' + e);
        return false;
    }
}
// 等 rwxp 转译缓存出现 (游戏启动后 10-25s)
var tries = 0;
var hooked = false;
var iv = setInterval(function () {
    tries++;
    if (tries % 5 === 0) L('[tick] ' + tries + 's');
    if (!hooked) {
        hooked = scanAndHook();
        if (hooked) {
            L('[+] 全部就绪, 等待解密...');
            clearInterval(iv);
        }
    }
    if (tries > 90) { clearInterval(iv); L('[-] 90s 超时'); }
}, 1000);
