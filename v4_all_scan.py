# -*- coding: utf-8 -*-
# v4: 全 rwx 区扫描 + 多模式 (8b16/8b56/8b46/8b76/8b86/8b96) + 5s 轮询
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
var logfile = '/data/data/com.netease.tom/files/keyhook5.txt';
function log(s) {
    try {
        var f = new File(logfile, 'a');
        f.write(s + '\n');
        f.close();
    } catch (e) {}
}
log('[+] v4 load ' + Date.now());
['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var a = Module.findExportByName(null, n);
        if (a) Interceptor.replace(a, new NativeCallback(function () { log('[kill blocked] ' + n); }, 'int', ['int']));
    } catch (e) {}
});
var hooked = {};
function hookKeyAt(addr, pat) {
    var k = addr.toString();
    if (hooked[k]) return;
    hooked[k] = 1;
    try {
        Interceptor.attach(addr, {
            onEnter: function (args) {
                try {
                    var rsi = this.context.rsi;
                    if (rsi && !rsi.isNull()) {
                        var key = rsi.readByteArray(16);
                        log('[★KEY] ' + addr + ' [' + pat + '] rsi=' + rsi + ' key=' + key);
                    }
                } catch (e) {}
            }
        });
        log('[+] hooked ' + addr + ' [' + pat + ']');
    } catch (e) { log('[!] hookfail ' + addr); }
}
// 多模式: mov edx,[rsi] 系列
var pats = ['8b 16', '8b 56 08', '8b 46 04', '8b 76 08', '8b 86 ?? ?? 00 00', '8b 96 ?? ?? 00 00'];
function scanRound(round) {
    var ranges = Process.enumerateRanges('rwx');
    var total = 0;
    ranges.forEach(function (r) {
        // 只扫大转译区 (0x4000 和 0x7896)
        var ok = false;
        try {
            if (r.base.compare(ptr('0x400000000000')) >= 0 && r.base.compare(ptr('0x400100000000')) < 0) ok = true;
            if (r.base.compare(ptr('0x789000000000')) >= 0 && r.base.compare(ptr('0x789700000000')) < 0) ok = true;
        } catch (e) {}
        if (!ok) return;
        pats.forEach(function (p) {
            try {
                Memory.scan(r.base, r.size, p, {
                    onMatch: function (addr) {
                        total++;
                        if (total <= 800) hookKeyAt(addr, p);
                    },
                    onComplete: function () {}
                });
            } catch (e) {}
        });
    });
    log('[+] round ' + round + ' hits=' + total);
}
var round = 0;
var iv = setInterval(function () {
    round++;
    scanRound(round);
    log('[tick] ' + Date.now());
    if (round >= 20) clearInterval(iv);
}, 5000);
scanRound(0);
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
print('v4 loaded!', flush=True)
time.sleep(300)
