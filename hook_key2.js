// hook_key2.js — 固定基址版: 壳自定义加载 so, frida 枚举不到, 用 maps 已知基址
// 基址 0x400020e00000 (maps 确认固定); 偏移同 RUNTIME so
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

console.log("[+] 固定基址 = " + BASE);

// 1) 解密包装器 0x85261c: x1=data ptr, x2=key ptr(16B)
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
    console.log("[+] hook 解密包装器 0x85261c OK");
} catch (e) {
    console.log("[-] hook 解密失败: " + e);
}

// 2) XXTEAUtil 单例: 全局指针 0x1095c20 → 实例
try {
    var gptr = BASE.add(0x1095c20);
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
    console.log("[-] XXTEAUtil 读取失败: " + e);
}

console.log("[+] 就绪, 等待解密触发...");
