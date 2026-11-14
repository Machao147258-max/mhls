// tb_tom_probe: attach 试探（只读）——模块/内存布局摘要
function log(msg) { console.log(msg); }

setTimeout(function() {
    log('[*] tb_tom_probe attach ok');
    try {
        var mods = Process.enumerateModules();
        log('[+] 模块数: ' + mods.length);
        // 关键模块摘要
        var interesting = [];
        mods.forEach(function(m) {
            if (/cocos|sec|sec-lib|secsdk|unisec|ybuaxz|NgModules|xdl|g(name|um)|frida|netease|nettomb|patcher|netease/.test(m.name)) {
                interesting.push({n: m.name, base: m.base.toString(), size: m.size});
            }
        });
        interesting.sort(function(a, b) { return b.size - a.size; });
        interesting.slice(0, 25).forEach(function(m) {
            log('  ' + m.n + '  base=' + m.base + '  size=' + (m.size / 1024 / 1024).toFixed(1) + 'MB');
        });
    } catch(e) { log('[-] mods: ' + e); }

    // 内存布局摘要（大类）
    try {
        var totalR = 0, totalRW = 0, totalX = 0;
        var ranges = Process.enumerateRanges('---');
        ['r--', 'rw-', 'r-x'].forEach(function(p) {
            var rs = Process.enumerateRanges(p);
            var sz = 0;
            rs.forEach(function(r) { sz += r.size; });
            log('[+] ' + p + ': ' + rs.length + ' 段, ' + (sz / 1024 / 1024).toFixed(1) + 'MB');
        });
    } catch(e) { log('[-] mem: ' + e); }

    log('[*] done');
}, 3000);