// xxtea_hook.js — hook XXTEA 函数 (libcocos2dlua 0x850abc) 捕获 key 参数
var LF = '/data/data/com.netease.tom/files/xxtea_hook.txt';
var f = new File(LF, 'a');
function L(s) { try { f.write(s + '\n'); f.flush(); } catch (e) {} }
L('[+] xxtea_hook ' + Date.now());

// 找 libcocos2dlua 基址
var base = null;
Process.enumerateModules().forEach(function (m) {
    if (/libcocos2dlua/.test(m.name)) base = m.base;
});
// enumerateModules 可能被隐藏 — 从 /proc/self/maps 读
if (!base) {
    try {
        var maps = new File('/proc/self/maps', 'r');
        var line;
        while ((line = maps.readLine()) !== null) {
            if (line.indexOf('libcocos2dlua.so') >= 0) {
                base = ptr(line.split('-')[0]);
                break;
            }
        }
        maps.close();
    } catch (e) { L('maps err ' + e); }
}
if (!base) { L('libcocos2dlua NOT FOUND'); } else {
    L('[BASE] libcocos2dlua @ ' + base);
    var fn = base.add(0x850abc);
    var fn2 = base.add(0x85397c);
    L('[HOOK] xxtea @ ' + fn + ' / ' + fn2);
    [fn, fn2].forEach(function (addr) {
        try {
            Interceptor.attach(addr, {
                onEnter: function (args) {
                    L('=== XXTEA CALL x0=' + args[0] + ' x1=' + args[1] + ' x2=' + args[2] + ' x3=' + args[3]);
                    try {
                        // key 候选: x1+0x28 和 x0+0x28 (16字节)
                        ['x1+0x28', 'x0+0x28'].forEach(function (tag) {
                            var p = tag[0] === 'x' ? (tag[1] === '1' ? args[1] : args[0]) : null;
                            if (p && !p.isNull()) {
                                var k = p.add(0x28).readByteArray(16);
                                var u = new Uint8Array(k);
                                var s = '';
                                for (var i = 0; i < 16; i++) s += ('0' + u[i].toString(16)).slice(-2);
                                L('  key[' + tag + '] ' + s);
                            }
                        });
                        // 也 dump x1 对象前 0x40
                        if (!args[1].isNull()) {
                            try {
                                var d = new Uint8Array(args[1].readByteArray(0x40));
                                var hx = '';
                                for (var i = 0; i < d.length; i++) hx += ('0' + d[i].toString(16)).slice(-2);
                                L('  obj[0x40] ' + hx);
                            } catch (e) {}
                        }
                    } catch (e) { L('  read err ' + e); }
                }
            });
            L('  attached ' + addr);
        } catch (e) {
            L('  attach FAIL ' + addr + ' ' + e);
        }
    });
}
L('[+] 就绪');