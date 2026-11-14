# -*- coding: utf-8 -*-
# spawn + 防自杀 + x86 key 点 hook (0x4f327b mov edx,[rsi])
import frida, sys, time

JS = r"""
'use strict';
var logfile = '/data/data/com.netease.tom/files/keyhook2.txt';
function log(s) {
    try {
        var f = new File(logfile, 'a');
        f.write(s + '\n');
        f.close();
    } catch (e) {}
}
log('[+] spawn keyhook ' + Date.now());

// 防自杀
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var a = Module.findExportByName(null, n);
        if (a) {
            Interceptor.replace(a, new NativeCallback(function () { log('[kill blocked] ' + n); }, 'int', ['int']));
        }
    } catch (e) {}
});

// hook x86 key 读点 (转译缓存)
var cands = [
    { base: 0x400060174000, off: 0x4f327b },   // mov edx,[rsi] key 加载
    { base: 0x400060174000, off: 0x4f335c },   // DELTA
];
setTimeout(function () {
    cands.forEach(function (c) {
        var addr = ptr(c.base + c.off);
        try {
            var m = Process.findRangeByAddress(addr);
            if (!m) { log('[!] 不可达 ' + addr); return; }
            var b = addr.readByteArray(8);
            log('[+] ' + addr + ' 指令: ' + b);
            Interceptor.attach(addr, {
                onEnter: function (args) {
                    try {
                        var rsi = this.context.rsi;
                        if (rsi.isNull() === false) {
                            var key = rsi.readByteArray(16);
                            log('[★KEY] rsi=' + rsi + ' key=' + key);
                        }
                    } catch (e) { log('[!] ' + e); }
                }
            });
            log('[+] hooked ' + addr);
        } catch (e) { log('[!] hook ' + addr + ' ' + e); }
    });
    log('[+] done');
}, 3000);

// 保持 alive: 周期日志
setInterval(function () { log('[tick] ' + Date.now()); }, 30000);
"""

def main():
    dev = frida.get_device_manager().add_remote_device('127.0.0.1:45679')
    print('spawn com.netease.tom...')
    pid = dev.spawn('com.netease.tom')
    print('spawned pid', pid)
    session = dev.attach(pid)
    script = session.create_script(JS)
    script.on('message', lambda m, d: print('[msg]', m))
    script.load()
    dev.resume(pid)
    print('resumed! 观察中 (Ctrl+C 退出)')
    time.sleep(240)

if __name__ == '__main__':
    main()