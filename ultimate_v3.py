# -*- coding: utf-8 -*-
# 终极 v3: 启动早期 attach → 多轮扫描转译区(等 XXTEA 代码生成) → hook 全部 8b16
# 流程: 先 force-stop → monkey → 立即 attach → v3 hook(每 20s 重扫, 共 10 轮)
import frida, subprocess, time, sys

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
def sh(args, t=20):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return 'ERR'

JS = r"""
'use strict';
var logfile = '/data/data/com.netease.tom/files/keyhook4.txt';
function log(s) {
    try {
        var f = new File(logfile, 'a');
        f.write(s + '\n');
        f.close();
    } catch (e) {}
}
log('[+] v3 load ' + Date.now());

['exit', '_exit', 'abort', 'raise', 'pthread_kill', 'tgkill', 'kill'].forEach(function (n) {
    try {
        var a = Module.findExportByName(null, n);
        if (a) Interceptor.replace(a, new NativeCallback(function () { log('[kill blocked] ' + n); }, 'int', ['int']));
    } catch (e) {}
});

var hooked = {};
function hookKeyAt(addr) {
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
                        log('[★KEY] ' + addr + ' rsi=' + rsi + ' key=' + key);
                    }
                } catch (e) {}
            }
        });
        log('[+] hooked ' + addr);
    } catch (e) { log('[!] hookfail ' + addr + ' ' + e); }
}

function scanRound(round) {
    var ranges = Process.enumerateRanges('rwx');
    var n = 0;
    ranges.forEach(function (r) {
        if (r.base.compare(ptr('0x400060000000')) >= 0 && r.base.compare(ptr('0x400070000000')) < 0) {
            try {
                Memory.scan(r.base, r.size, '8b 16', {
                    onMatch: function (addr) {
                        n++;
                        if (n <= 500) hookKeyAt(addr);
                    },
                    onComplete: function () {}
                });
            } catch (e) {}
        }
    });
    log('[+] round ' + round + ' 8b16=' + n);
}

var round = 0;
var iv = setInterval(function () {
    round++;
    log('[tick] ' + Date.now() + ' round=' + round);
    scanRound(round);
    if (round >= 15) clearInterval(iv);
}, 20000);
scanRound(0);
"""

def main():
    # 1. force-stop + 启动
    sh(['shell', 'su -c am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    print('已启动, 等待进程...')
    dev = frida.get_device_manager().add_remote_device('127.0.0.1:45679')
    pid = None
    for i in range(20):
        time.sleep(2)
        try:
            procs = dev.enumerate_processes()
            for p in procs:
                if p.name == 'com.netease.tom':
                    pid = p.pid
                    break
        except Exception:
            pass
        if pid:
            break
    print('pid:', pid)
    if not pid:
        print('进程未找到'); return
    print('立即 attach (启动早期, 应该快)...')
    session = dev.attach(pid)
    print('attached!')
    script = session.create_script(JS)
    script.on('message', lambda m, d: print('[msg]', m))
    script.load()
    print('v3 loaded! 保持 400s')
    time.sleep(400)

if __name__ == '__main__':
    main()