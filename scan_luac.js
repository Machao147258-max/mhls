// 内存扫描: 找解密后的 luac 脚本 (特征: 魔改 Lua 头, 标准 5.1 是 1b 4c 75 61)
// 猫和老鼠魔改 VM, 头可能是 1b 4c 75 61 或自定义
// 同时也找 x1v5fzto 大块 (未解密残留)
var ranges = Process.enumerateRanges('r--');
var found = 0;
ranges.forEach(function (r) {
    if (r.size > 4096 && r.size < 64 * 1024 * 1024) {
        try {
            // 读前 4096 找特征
            var b = r.base.readByteArray(Math.min(4096, r.size));
            if (b) {
                var arr = Array.prototype.slice.call(new Uint8Array(b));
                for (var i = 0; i < arr.length - 4; i++) {
                    if (arr[i] === 0x1b && arr[i + 1] === 0x4c && arr[i + 2] === 0x75 && arr[i + 3] === 0x61) {
                        console.log('LUAC? @' + r.base.add(i) + ' range=' + r.base + ' size=' + r.size);
                        found++;
                    }
                }
            }
        } catch (e) {}
    }
});
console.log('scan done found=' + found);