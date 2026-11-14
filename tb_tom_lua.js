// tb_tom_lua: hook Cocos2d-lua 脚本加载（抓脚本名/字节码）+ Lua 全局数值观察
function log(msg) { console.log(msg); }

setTimeout(function() {
    log('[*] tb_cocos 启动');
    var cocos = null;
    try { cocos = Process.findModuleByName('libcocos2dlua.so'); } catch(e) {}
    if (!cocos) {
        // x86_64 命名变体
        var mods = Process.enumerateModules();
        mods.forEach(function(m) {
            if (/cocos2dlua/.test(m.name) && !cocos) { cocos = m; }
        });
    }
    log('[+] cocos: ' + (cocos ? cocos.name : '未找到'));

    // Lua C API（从 cocos 导出表找）
    function findCocosExport(name) {
        if (!cocos) return null;
        try { var a = Module.findExportByName(cocos.name, name); if (a) return a; } catch(e) {}
        try { var b = cocos.getExportByName(name); if (b) return b; } catch(e) {}
        return null;
    }

    // 1. luaL_loadbuffer / luaL_loadstring（抓脚本）
    ['luaL_loadbuffer', 'luaL_loadbufferx', 'luaL_loadstring', 'lua_load'].forEach(function(fn) {
        var addr = findCocosExport(fn);
        if (!addr) return;
        Interceptor.attach(addr, {
            onEnter: function(a) {
                try {
                    var tag = 'L';
                    var s = null, len;
                    if (fn === 'luaL_loadbuffer' || fn === 'luaL_loadbufferx') {
                        s = a[2].readUtf8String(Math.min(a[3].toInt32(), 400));
                        len = a[3].toInt32();
                    } else {
                        s = a[2].readUtf8String(300);
                        len = s ? s.length : 0;
                    }
                    if (!s || s.length < 4) return;
                    // 判断字节码 or 明文
                    var isBytecode = s.charCodeAt(0) === 0x1b && s.charCodeAt(1) === 0x4c; // ESC L
                    log('\n[LUA ' + fn + '] len=' + len + (isBytecode ? ' [字节码]' : ' [明文]'));
                    var head = s.slice(0, 200).replace(/\n/g, ' | ');
                    log('  ' + head.slice(0, 250));
                } catch(e) {}
            }
        });
    });

    // 2. lua_getglobal（读全局变量——金币/钻石往往在此）
    var g = findCocosExport('lua_gettop');
    if (g) log('[+] lua_gettop 可用');
    var gg = findCocosExport('lua_getglobal');
    if (gg) {
        var names = {};
        Interceptor.attach(gg, {
            onEnter: function(a) {
                try {
                    var s = a[2].readUtf8String(80);
                    if (!s) return;
                    if (/coin|gold|diamond|money|level|hp|score|player|hero|skill|bag|count|user|id|name|nick/i.test(s)) {
                        names[s] = (names[s] || 0) + 1;
                        if (names[s] <= 3) log('[getglobal] ' + s);
                    }
                } catch(e) {}
            }
        });
        log('[+] lua_getglobal hook');
    }

    log('[*] 等待游戏操作（点击/加载主界面触发）');
}, 4000);