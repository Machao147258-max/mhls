# -*- coding: utf-8 -*-
# v5: attach(0.2s) → 等 25s(解密窗口) → 单次扫描 DELTA(9e3779b9 立即数) + key 读(8b16) → hook 全部
import frida, subprocess, time, sys

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
def sh(args, t=15):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return 'ERR'

def get_pid():
    p = sh(['shell', 'su -c pidof com.netease.tom']).strip()
    for t in p.split():
        if t.isdigit():
            return int(t)
    return None

JS = r"""
'use strict';
var logfile = '/data/data/com.netease.tom/files/keyhook6.txt';
function log(s) {
    try {
        var f = new File(logfile, 'a');
        f.write(s + '\n');
        f.close();
    } catch (e) {}
}
log('[+] v5 load ' + Date.now());
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var a = Module.findExportByName(null, n);
        if (a) Interceptor.replace(a, new NativeCallback(function () { log('[kill blocked] ' + n); }, 'int', ['int']));
    } catch (e) {}
});
var hooked = {};
function hookAt(addr, tag) {
    var k = addr.toString();
    if (hooked[k]) return;
    hooked[k] = 1;
    try {
        Interceptor.attach(addr, {
            onEnter: function (args) {
                try {
                    var ctx = this.context;
                    var rsi = ctx.rsi;
                    var rdi = ctx.rdi;
                    var out = [];
                    if (rsi && !rsi.isNull()) {
                        try { out.push('rsi16=' + rsi.readByteArray(16)); } catch (e) {}
                    }
                    if (rdi && !rdi.isNull()) {
                        try { out.push('rdi16=' + rdi.readByteArray(16)); } catch (e) {}
                    }
                    if (out.length) log('[★] ' + addr + ' [' + tag + '] ' + out.join(' '));
                } catch (e) {}
            }
        });
        log('[+] hooked ' + addr + ' [' + tag + ']');
    } catch (e) { log('[!] hookfail ' + addr); }
}
// 等 25 秒后单次扫描
setTimeout(function () {
    log('[scan] start ' + Date.now());
    var ranges = Process.enumerateRanges('rwx');
    var n = 0;
    ranges.forEach(function (r) {
        var base = r.base;
        try {
            var inRange = (base.compare(ptr('0x400000000000')) >= 0 && base.compare(ptr('0x400100000000')) < 0) ||
                          (base.compare(ptr('0x789000000000')) >= 0 && base.compare(ptr('0x78a000000000')) < 0);
        } catch (e) { return; }
        if (!inRange) return;
        // DELTA 立即数 + key 读
        ['b9 79 37 9e', 'ba 79 37 9e', '8b 16'].forEach(function (p) {
            try {
                Memory.scan(r.base, r.size, p, {
                    onMatch: function (addr) { n++; if (n <= 500) hookAt(addr, p); },
                    onComplete: function () {}
                });
            } catch (e) {}
        });
    });
    log('[scan] done n=' + n + ' ' + Date.now());
}, 25000);
setInterval(function () { log('[tick] ' + Date.now()); }, 30000);
"""

sh(['shell', 'su -c am force-stop com.netease.tom'])
time.sleep(3)
sh(['shell', 'monkey -p com.netease.tom 1'])
print('monkey 已发', flush=True)
dev = frida.get_device_manager().add_remote_device('127.0.0.1:45680')
pid = None
t0 = time.time()
while time.time() - t0 < 30:
    pid = get_pid()
    if pid:
        break
    time.sleep(0.5)
print('pid:', pid, '%.1fs' % (time.time() - t0), flush=True)
session = dev.attach(pid)
print('attached!', flush=True)
script = session.create_script(JS)
script.on('message', lambda m, d: print('[msg]', m, flush=True))
script.load()
print('v5 loaded!', flush=True)
time.sleep(300)
