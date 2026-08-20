// tb_tom_lib: hook dlopen 观察游戏引擎加载序列
function log(msg) { console.log(msg); }

setTimeout(function() {
    log('[*] tb_tom_lib');
    var libs = {};
    ['dlopen', '__loader_dlopen', 'android_dlopen_ext'].forEach(function(fn) {
        var a = Module.findExportByName('libdl.so', fn);
        if (!a) return;
        Interceptor.attach(a, {
            onEnter: function(args) {
                try {
                    var s = args[0].readUtf8String(200);
                    if (!s) return;
                    s = s.replace(/\/data\/app[^\s]*?\/(.*?\.so)/, '$1');
                    if (s.indexOf('.so') === -1) return;
                    // game relevant only
                    if (/cocos|sec|unisec|tom|netease|NgModules|ybuaxz|sec-lib|secsdk|java|patcher|xdl/i.test(s)) {
                        log('[DLOPEN] ' + s);
                    }
                } catch(e) {}
            }
        });
    });
    log('[+] dlopen hooked - waiting game engine load');
}, 3000);