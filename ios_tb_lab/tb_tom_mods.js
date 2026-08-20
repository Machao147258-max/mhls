// tb_tom_mods: list all modules (find game engine / renamed cocos)
function log(msg) { console.log(msg); }

setTimeout(function() {
    log('[*] tb_tom_mods start');
    var mods = Process.enumerateModules();
    log('[+] total: ' + mods.length);
    mods.forEach(function(m) {
        var n = m.name;
        if (n.length < 4) return;
        if (n.indexOf('.so') === -1) return;
        // skip obvious system libs
        var skip = ['libandroid','liblog.','libc++','libdl','libm.','libstdc','libz.','libgcc','libexpat','libpng','libjpg','libjpeg','libssl','libcrypto','libicu','libnativeh','libjnigraphics','libhwui','libskia','libGLES','libEGL','libvulkan','libOpenSL','libaudioclient','libbinder','libcutils','libutils','libselinux','libbase','libnetd','libziparchive','libchrome','libsqlite','libcompiler','libunwind','libbacktrace','libtinyxml','libart','libdexfile','libopenjdk','libicu_jni','libjavacore','libicui18n','libjnidispatcher','libamidi','libaudiomanager','libbluetooth','libcamera','libharfbuzz','libheif','libmemunreachable','libnativeloader','libnativebridge','libneuralnetworks','libperf','libserialport','libstats','libvixl','libweakref','libclang_rt','libdruntime','libprofile','libhwjpg']
        var ok = true;
        for (var i = 0; i < skip.length; i++) if (n.indexOf(skip[i]) === 0) { ok = false; break; }
        if (!ok) return;
        log('  ' + n);
    });
    log('[*] done');
}, 4000);