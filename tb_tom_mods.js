// tb_tom_mods: 列出全部模块名（找游戏引擎/疑似改名的 cocos）
function log(msg) { console.log(msg); }

setTimeout(function() {
    log('[*] tb_tom_mods');
    var mods = Process.enumerateModules();
    log('[+] 总数: ' + mods.length);
    mods.forEach(function(m) {
        var n = m.name;
        if (n.length < 4) return;
        // 过滤系统噪音
        if (/^lib(android|log|c\+\+|dl|m|stdc|z|gcc|expat|png|jpg|ssl|crypto|icui|icu|zix|native|jnigraphics|hwui|skia|egl|gl|GLES|vulkan|OpenSL|audioclient|binder|hwbinder|cutils|utils|selinux|base|netd|ziparchive|chrome|sqlite|compiler|unwind|backtrace)/.test(n)) return;
        log('  ' + n);
    });
    log('[*] done', 8000);