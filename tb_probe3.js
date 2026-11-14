// tb_probe3: 内存生化扫描 Lua 字节码头 + 全模块按体积排序
function log(m) { console.log(m); }

setTimeout(function () {
    log('[*] tb_probe3 attach ok');

    // 1. 全模块按体积排
    var mods = Process.enumerateModules();
    mods.sort(function (a, b) { return b.size - a.size; });
    log('[+] 模块按体积 Top18:');
    mods.slice(0, 18).forEach(function (m) {
        log('    ' + m.name + '  ' + (m.size / 1024 / 1024).toFixed(1) + 'MB  base=' + m.base);
    });

    // 2. 扫内存: Lua5.1(1b 4c 75 61) / Lua 5.2(1b 4c 75 61 52)? 实际 5.1:1b 4c 75 61 51; LuaJIT: 1b 4c 4a
    var pats = {
        'Lua5.1字节码': '1b 4c 75 61 51',
        'Lua5.2字节码': '1b 4c 75 61 52',
        'LuaJIT字节码': '1b 4c 4a 01',
    };
    var totalFound = {};
    Object.keys(pats).forEach(function (k) { totalFound[k] = 0; });

    var ranges = Process.enumerateRanges('rw-');
    var skipped = 0;
    ranges.forEach(function (r) {
        if (r.size > 128 * 1024 * 1024) { skipped++; return; }
        Object.keys(pats).forEach(function (k) {
            if (totalFound[k] > 30) return;
            try {
                var hits = Memory.scanSync(r.base, r.size, pats[k]);
                if (hits.length) {
                    log('[!] ' + k + ' ×' + hits.length + '  @ ' + r.base + ' size=' + r.size);
                    hits.slice(0, 6).forEach(function (h) {
                        var b = h.address.readByteArray(64);
                        var bytes = Array.from(new Uint8Array(b)).map(function (x) { return x.toString(16).padStart(2, '0'); }).join(' ');
                        log('      @' + h.address + '  ' + bytes);
                    });
                    totalFound[k] += hits.length;
                }
            } catch (e) {}
        });
    });
    log('[+] 扫描完成: ' + JSON.stringify(totalFound) + ' (跳过超大段 ' + skipped + ')');

    // 3. 找 'system/script' 字符串(定位 ARM 引擎 rodata)
    try {
        var rr = Process.enumerateRanges('r--');
        var shown = 0;
        rr.forEach(function (r) {
            if (shown >= 8 || r.size > 256 * 1024 * 1024) return;
            try {
                var hits = Memory.scan(r.base, Math.min(r.size, 8 * 1024 * 1024), '73 79 73 74 65 6d 2f 73 63 72 69 70 74');
                if (hits.length) {
                    var m = Process.findRangeByAddress(hits[0].address);
                    log('[!] system/script 字符串 @' + hits[0].address + (m ? (' in ' + m.file.path) : ' (匿名)'));
                    shown++;
                }
            } catch (e) {}
        });
        if (!shown) log('[-] system/script 未在 r-- 前8MB内命中(可能更深或加密)');
    } catch (e) { log('err3 ' + e); }

    log('[*] done');
}, 2500);