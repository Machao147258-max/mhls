// hook_key4.js — 全目标 hook + 基址轮询 (启动期抓解密)
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
function waitBase(cb) {
    var t = 0;
    var iv = setInterval(function () {
        t += 200;
        try {
            var m = BASE.readU32();
            if (m === 0x464c457f) {
                clearInterval(iv);
                console.log("[+] 基址就绪 @" + BASE + " (" + t + "ms)");
                cb();
            }
        } catch (e) {}
        if (t > 90000) { clearInterval(iv); console.log("[-] 基址超时"); }
    }, 200);
}
function doHook() {
    var targets = {
        'reader': 0x852548, 'decwrap': 0x85261c, 'stream': 0x8ab25c,
        'blk108': 0x8ab108, 'blk14f4': 0x8b14f4, 'luadec': 0x4095b0,
        'luaenc': 0x408ddc, 'encxt': 0x3fc774, 'encwrap': 0x8529cc
    };
    Object.keys(targets).forEach(function (k) {
        try {
            Interceptor.attach(BASE.add(targets[k]), {
                onEnter: function (args) {
                    try {
                        if (k === 'reader' && args[1].toInt32() === 16) {
                            var kb = args[0].readByteArray(16);
                            console.log("[★reader16] " + JSON.stringify(toStr(kb)) + " hex=" + hex(kb));
                        } else if (k === 'reader') {
                            console.log("[reader] len=" + args[1].toInt32() + " flag=" + args[2]);
                        } else if (k === 'decwrap') {
                            var kb = args[2].readByteArray(16);
                            console.log("[★decwrap] data=" + args[1] + " key=" + JSON.stringify(toStr(kb)) + " hex=" + hex(kb));
                        } else if (k === 'stream' || k === 'blk108' || k === 'blk14f4') {
                            console.log("[" + k + "] x0=" + args[0] + " x1=" + args[1] + " x2=" + args[2]);
                        } else {
                            console.log("[" + k + "] 调用 L=" + args[0]);
                        }
                    } catch (e) {
                        console.log("[" + k + "] err " + e);
                    }
                }
            });
            console.log("[+] hook " + k + " OK");
        } catch (e) {
            console.log("[-] hook " + k + " 失败: " + e);
        }
    });
    console.log("[+] 全部就绪");
}
waitBase(doHook);
