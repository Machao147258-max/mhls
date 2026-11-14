// hook_key3.js — 多目标 hook + 基址轮询
// 目标: 0x852548 reader(必经), 0x85261c 解密包装, 0x4095b0 decryptStringWithKeyLua 注册, 0x8ab108 块核心
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

// 轮询基址可读 (ELF 魔数)
function waitBase(cb) {
    var t = 0;
    var iv = setInterval(function () {
        t += 500;
        try {
            var m = BASE.readU32();
            if (m === 0x464c457f) {  // \x7fELF
                clearInterval(iv);
                console.log("[+] 基址就绪 @ " + BASE + " (after " + t + "ms)");
                cb();
            }
        } catch (e) {}
        if (t > 60000) {
            clearInterval(iv);
            console.log("[-] 基址 60s 未就绪");
        }
    }, 500);
}

function doHook() {
    // 1) reader 0x852548: x0=src, w1=len, w2=flag, x3=out
    try {
        Interceptor.attach(BASE.add(0x852548), {
            onEnter: function (args) {
                var len = args[1].toInt32();
                if (len === 16) {
                    try {
                        var b = args[0].readByteArray(16);
                        console.log("[READER16] src=" + args[0] + " len=16 data=" + JSON.stringify(toStr(b)) + " hex=" + hex(b));
                    } catch (e) {
                        console.log("[READER16] src=" + args[0] + " err " + e);
                    }
                } else {
                    console.log("[READER] src=" + args[0] + " len=" + len + " flag=" + args[2]);
                }
            }
        });
        console.log("[+] hook reader 0x852548 OK");
    } catch (e) { console.log("[-] reader hook err " + e); }

    // 2) 解密包装 0x85261c
    try {
        Interceptor.attach(BASE.add(0x85261c), {
            onEnter: function (args) {
                try {
                    var kb = args[2].readByteArray(16);
                    console.log("[DEC] data=" + args[1] + " key=" + JSON.stringify(toStr(kb)) + " hex=" + hex(kb));
                } catch (e) {
                    console.log("[DEC] data=" + args[1] + " key=?? err=" + e);
                }
            }
        });
        console.log("[+] hook 0x85261c OK");
    } catch (e) { console.log("[-] 0x85261c err " + e); }

    // 3) decryptStringWithKeyLua 注册入口 0x4095b0 (Lua C 函数, args[0]=L)
    try {
        Interceptor.attach(BASE.add(0x4095b0), {
            onEnter: function (args) {
                console.log("[LUA-dec] 调用! L=" + args[0]);
            }
        });
        console.log("[+] hook 0x4095b0 OK");
    } catch (e) { console.log("[-] 0x4095b0 err " + e); }

    // 4) 块核心 0x8ab108
    try {
        Interceptor.attach(BASE.add(0x8ab108), {
            onEnter: function (args) {
                console.log("[BLK] 0x8ab108 调用 x0=" + args[0] + " x1=" + args[1]);
            }
        });
        console.log("[+] hook 0x8ab108 OK");
    } catch (e) { console.log("[-] 0x8ab108 err " + e); }

    // 5) XXTEAUtil 单例
    try {
        var gptr = BASE.add(0x1095c20);
        var inst = gptr.readPointer();
        if (!inst.isNull()) {
            console.log("[+] XXTEAUtil 实例 @" + inst);
            var kcount = inst.add(0x24).readU32();
            var scount = inst.add(0x28).readU32();
            var ktable = inst.add(0x30).readPointer();
            var stable = inst.add(0x38).readPointer();
            var all = [];
            for (var i = 0; i < Math.min(kcount, 64) && !ktable.isNull(); i++) {
                try {
                    var p = ktable.add(i * 8).readPointer();
                    if (p.isNull()) break;
                    var b = p.readByteArray(16);
                    all.push(hex(b));
                    console.log("    key[" + i + "] " + JSON.stringify(toStr(b)) + " hex=" + hex(b));
                } catch (e) {}
            }
            var secAll = [];
            for (var i = 0; i < Math.min(scount, 16) && !stable.isNull(); i++) {
                try {
                    var p = stable.add(i * 8).readPointer();
                    if (p.isNull()) break;
                    var b = p.readByteArray(16);
                    secAll.push(hex(b));
                } catch (e) {}
            }
            console.log("[★] KEYS=" + JSON.stringify(all));
            console.log("[★] SECRETS=" + JSON.stringify(secAll));
        } else {
            console.log("[-] XXTEAUtil 全局指针为 0");
        }
    } catch (e) { console.log("[-] XXTEAUtil err " + e); }

    console.log("[+] 全部就绪, 等待触发...");
}

waitBase(doHook);
