// hook_key.js — 抓取解密 key: hook 解密包装器 0x85261c (参数 x2=16B key)
// 用法: frida -H 127.0.0.1:31337 -p <PID> -l hook_key.js
setTimeout(function () {
    var lib = Process.findModuleByName("libcocos2dlua.so");
    if (!lib) {
        console.log("[-] libcocos2dlua.so 未加载");
        Process.enumerateModules().slice(0, 40).forEach(function (m) { console.log("  mod:", m.name); });
        return;
    }
    var base = lib.base;
    console.log("[+] libcocos2dlua.so base = " + base + " size = " + lib.size);

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

    // 1) 解密包装器 0x85261c: x1=data, x2=key(16B), x3=?
    var dec = base.add(0x85261c);
    Interceptor.attach(dec, {
        onEnter: function (args) {
            try {
                var kb = args[2].readByteArray(16);
                console.log("[DEC] data=" + args[1] + " key=" + JSON.stringify(toStr(kb)) + " hex=" + hex(kb));
            } catch (e) {
                console.log("[DEC] data=" + args[1] + " key=?? err=" + e);
            }
        }
    });
    console.log("[+] 已 hook 解密包装器 0x85261c");

    // 2) XXTEAUtil 单例 (0x1095c20 全局指针 → 实例)
    try {
        var gptr = base.add(0x1095c20);
        var inst = gptr.readPointer();
        console.log("[+] XXTEAUtil 实例 @" + inst);
        var kcount = inst.add(0x24).readU32();
        var scount = inst.add(0x28).readU32();
        console.log("[+] keyCount=" + kcount + " secretCount=" + scount);
        var ktable = inst.add(0x30).readPointer();
        var stable = inst.add(0x38).readPointer();
        var all = [];
        for (var i = 0; i < Math.min(kcount, 64) && !ktable.isNull(); i++) {
            try {
                var p = ktable.add(i * 8).readPointer();
                if (p.isNull()) break;
                var b = p.readByteArray(16);
                console.log("    key[" + i + "] " + JSON.stringify(toStr(b)) + " hex=" + hex(b));
                all.push(hex(b));
            } catch (e) { console.log("    key[" + i + "] err " + e); }
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
    } catch (e) {
        console.log("[+] XXTEAUtil 读取失败: " + e);
    }

    console.log("[+] 就绪, 等待解密触发 (游戏加载/切场景时)...");
}, 1000);
