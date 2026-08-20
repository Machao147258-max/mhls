// tb_tom_engine: 找 cocos 基址（maps 无法——用 frida 枚举重试 + ELF 扫描）
function log(msg) { console.log(msg); }

setTimeout(function() {
    log('[*] tb_tom_engine');
    // 方式1: enumerateModules
    var found = null;
    try {
        var mods = Process.enumerateModules();
        mods.forEach(function(m) {
            if (/cocos|lua/i.test(m.name) && !found) {
                found = {name: m.name, base: m.base, size: m.size};
                log('[+] frida枚举: ' + m.name + ' @' + m.base + ' ' + (m.size/1048576).toFixed(1) + 'MB');
            }
        });
    } catch(e) { log('[-] enum: ' + e); }

    // 方式2: 读 /proc/self/maps 找 cocos（手动解析基址）
    if (!found) {
        try {
            var maps = Memory.readUtf8String? null : null;
            var f = new File('/proc/self/maps', 'r');
            var line;
            while ((line = f.readLine()) !== null) {
                if (line.indexOf('libcocos2dlua') !== -1 || line.indexOf('libsecsdk') !== -1) {
                    var m = line.match(/^([0-9a-f]+)-([0-9a-f]+)\s+([r-xwsp-]+)/);
                    if (m) {
                        log('[MAPS] ' + line.trim().slice(0, 130));
                        if (line.indexOf('r-x') !== -1) {
                            var base = ptr('0x' + m[1]);
                            var size = parseInt(m[2], 16) - parseInt(m[1], 16);
                            log('  base=' + base + ' size=' + size);
                            if (/cocos/.test(line)) found = {name: 'libcocos2dlua.so', base: base, size: size};
                        }
                    }
                }
            }
            f.close();
        } catch(e) { log('[-] maps: ' + e); }
    }

    // 方式3: dladdr 遍历（找包含 luaL_loadbuffer 的模块）
    if (!found) {
        try {
            var dladdr = new NativeFunction(Module.findExportByName(null, 'dladdr'), 'int', ['pointer', 'pointer']);
            var sym = Module.findExportByName(null, 'dlopen');
            var info = Memory.alloc(Process.pointerSize * 8);
            if (sym && dladdr(sym, info) > 0) {
                var fname = info.add(Process.pointerSize).readPointer().readUtf8String();
                log('[dladdr] dlopen 在: ' + fname);
            }
        } catch(e) {}
    }

    // 尝试 hook cocos 导出（通过扫描）
    log('[*] done, found=' + (found ? found.name : 'none'));
}, 4000);