// tb_probe2: 全模块导出符号扫描,定位真实 lua 引擎(不依赖模块名)
function log(m) { console.log(m); }

setTimeout(function () {
    log('[*] tb_probe2 attach ok');
    var mods = Process.enumerateModules();
    log('[+] 模块数: ' + mods.length);

    var skip = /^lib(android|art|binder|c$|c\+\+|dl|log|m$|stdc|z$|gcc|expat|png|jpeg|ssl|crypto|icu|monochrome|webview|hwui|skia|egl|GLES|vulkan|OpenSL|jnigraphics|ziparchive|compiler|unwind|backtrace|base|cutils|utils|selinux|netd)/;
    var luaPat = /^(lua[lA-Z_]|luaopen_|tolua_|lua_State)/;
    var engineHits = [];

    mods.forEach(function (m) {
        if (skip.test(m.name)) return;
        if (/lua|cocos|engine|tcb|hp1|unisec|spine|ck|sing|tom/i.test(m.name)) {
            log('[mod] ' + m.name + '  base=' + m.base + '  ' + Math.round(m.size / 1024 / 1024 * 10) / 10 + 'MB');
        }
        var exps = [];
        try { exps = m.enumerateExports(); } catch (e) { return; }
        if (!exps.length) return;
        var lua = exps.filter(function (e) {
            return luaPat.test(e.name) || /cocos|Lua|lua/i.test(e.name);
        });
        if (lua.length) {
            engineHits.push([m.name, lua.length]);
            log('  ★ ' + m.name + '  命中 ' + lua.length + ' 个 lua 导出');
            lua.slice(0, 10).forEach(function (e) { log('      ' + e.name); });
        }
    });

    // 兜底:所有模块里找任意含 lua 字符串的导出
    log('[+] 引擎候选: ' + (engineHits.length ? engineHits.map(function (h) { return h[0] + '(' + h[1] + ')'; }).join(' ') : '无'));

    // 内存里直接搜 lua 头签名(找不到导出时的兜底)
    try {
        var ranges = Process.enumerateRanges('r--');
        var found = 0;
        ranges.some(function (r) {
            if (r.size > 64 * 1024 * 1024) return false;
            try {
                var bytes = r.readByteArray(0);  // 只读第一页作采样,全量太慢
            } catch (e) { return false; }
            return false;
        });
        log('[+] 内存扫描略过(导出法已足够)');
    } catch (e) {}

    log('[*] done');
    process.exit(0);
}, 3000);