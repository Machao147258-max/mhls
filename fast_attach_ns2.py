# -*- coding: utf-8 -*-
# ns2 版快速 attach (45680)
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
print('pid:', pid, '耗时 %.1fs' % (time.time() - t0), flush=True)
if not pid:
    sys.exit(1)
t1 = time.time()
print('attach...', flush=True)
session = dev.attach(pid)
print('attached! %.1fs' % (time.time() - t1), flush=True)
JS = open(r'C:\Users\20751\Desktop\猫和老鼠\ultimate_v3.py', encoding='utf-8').read().split('JS = r"""')[1].split('"""')[0]
script = session.create_script(JS)
script.on('message', lambda m, d: print('[msg]', m, flush=True))
script.load()
print('v3 loaded!', flush=True)
time.sleep(420)
