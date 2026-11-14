// tb_watch: 观察检测线程 —— 记录 /proc/ 与检测相关路径的 open/fopen,按线程统计
function log(m) { console.log(m); }

setTimeout(function () {
    log('[*] tb_watch attach ok');
    var tidName = {};
    Process.enumerateThreads().forEach(function (t) { tidName[t.id] = t.name; });
    log('[+] 线程数: ' + Object.keys(tidName).length);

    var perTid = {};
    var paths = {};
    var total = 0;
    var LOG_CAP = 400;

    function hit(tid, path, fn) {
        total++;
        perTid[tid] = (perTid[tid] || 0) + 1;
        var p = paths[path] || 0;
        paths[path] = p + 1;
        if (samples < LOG_CAP) {
            samples++;
            log('[' + fn + '] tid=' + tid + ' (' + (tidName[tid] || '?') + ') ' + path);
        }
    }
    var samples = 0;

    function attachOpenat() {
        try {
            var m = Process.findModuleByName('libc.so');
            if (!m) return log('[-] libc 未找到');
            ['openat', '_openat', '__openat_64'].forEach(function (nm) {
                try {
                    var p = Module.findExportByName('libc.so', nm);
                    if (!p || p.isNull()) return;
                    Interceptor.attach(p, {
                        onEnter: function (a) {
                            try {
                                var path = a[1].readUtf8String(0x100);
                                if (!path) return;
                                if (/\/proc\//.test(path) || /trace|detect|sec|guard/i.test(path) ||
                                    /\/data\/local\/tmp\//.test(path)) {
                                    hit(Process.getCurrentThreadId(), path, nm);
                                }
                            } catch (e) {}
                        }
                    });
                    log('[+] hook ' + nm);
                } catch (e) {}
            });
            return true;
        } catch (e) { log('err ' + e); return false; }
    }

    if (attachOpenat()) {
        log('[*] 观察 40 秒…');
        setTimeout(function () {
            log('');
            log('=== 汇总: 按线程 ===');
            Object.keys(perTid).sort(function (a, b) { return perTid[b] - perTid[a]; }).slice(0, 15).forEach(function (t) {
                log('   tid ' + t + ' (' + (tidName[t] || '?') + '): ' + perTid[t]);
            });
            log('=== 路径 TOP ===');
            Object.keys(paths).sort(function (a, b) { return paths[b] - paths[a]; }).slice(0, 20).forEach(function (p) {
                log('   ' + paths[p] + 'x  ' + p);
            });
            log('[+] 总计命中 ' + samples + ' (截断于 ' + LOG_CAP + ')');
        }, 40000);
    }
}, 4000);