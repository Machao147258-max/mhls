# -*- coding: utf-8 -*-
# 全自动 v2: attach 后扫描转译区 (mov edx,[rsi] / DELTA) + hook 全部 + 防自杀 + 保持
import frida, sys, time

JS = r"""
'use strict';
var logfile = '/data/data/com.netease.tom/files/keyhook3.txt';
function log(s) {
    try {
        var f = new File(logfile, 'a');
        f.write(s + '\n');
        f.close();
    } catch (e) {}
}
log('[+] v2 load ' + Date.now());

['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var a = Module.findExportByName(null, n);
        if (a) Interceptor.replace(a, new NativeCallback(function () { log('[kill blocked] ' + n); }, 'int', ['int']));
    } catch (e) {}
});

function hookKeyAt(addr) {
    try {
        Interceptor.attach(addr, {
            onEnter: function (args) {
                try {
                    var rsi = this.context.rsi;
                    if (rsi && !rsi.isNull()) {
                        var key = rsi.readByteArray(16);
                        log('[★KEY] ' + addr + ' rsi=' + rsi + ' key=' + key);
                    }
                } catch (e) {}
            }
        });
        log('[+] hooked ' + addr);
    } catch (e) { log('[!] ' + addr + ' ' + e); }
}

setTimeout(function () {
    // 扫描转译区 mov edx,[rsi] = 8b 16
    var ranges = Process.enumerateRanges('rwx');
    var scanned = 0, found8b16 = 0;
    ranges.forEach(function (r) {
        if (r.base.compare(ptr('0x400060000000')) >= 0 && r.base.compare(ptr('0x400070000000')) < 0) {
            try {
                Memory.scan(r.base, r.size, '8b 16', {
                    onMatch: function (addr, size) {
                        found8b16++;
                        if (found8b16 <= 200) hookKeyAt(addr);
                    },
                    onComplete: function () {}
                });
                scanned++;
            } catch (e) {}
        }
    });
    log('[+] scan done: ' + scanned + ' ranges, 8b16=' + found8b16);

    // DELTA 模式 b9 79 37 9e (mov ecx/edx, 9e3779b9)
    var dcount = 0;
    ranges.forEach(function (r) {
        if (r.base.compare(ptr('0x400060000000')) >= 0 && r.base.compare(ptr('0x400070000000')) < 0) {
            try {
                Memory.scan(r.base, r.size, 'b9 79 37 9e', {
                    onMatch: function (addr) {
                        dcount++;
                        try {
                            Interceptor.attach(addr, {
                                onEnter: function () { log('[DELTA] ' + addr); }
                            });
                        } catch (e) {}
                    },
                    onComplete: function () {}
                });
            } catch (e) {}
        }
    });
    log('[+] delta hook: ' + dcount);
    log('[+] all done');
}, 2000);

setInterval(function () { log('[tick] ' + Date.now()); }, 30000);
"""

def main():
    dev = frida.get_device_manager().add_remote_device('127.0.0.1:45679')
    pid = int(sys.argv[1])
    print('attach', pid, '(等 2-4 分钟)...')
    session = dev.attach(pid)
    print('attached!')
    script = session.create_script(JS)
    script.on('message', lambda m, d: print('[msg]', m))
    script.load()
    print('loaded, 保持 360s')
    time.sleep(360)

if __name__ == '__main__':
    main()