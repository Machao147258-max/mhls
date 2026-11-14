# -*- coding: utf-8 -*-
# fast attach: force-stop → monkey → 0.5s 轮询 pid → 立即 attach → v3 hook
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

# 等上一个 session 的进程死(7555 的 job 24 可能还活着——force-stop 会杀它)
sh(['shell', 'su -c am force-stop com.netease.tom'])
time.sleep(3)
# 启动
sh(['shell', 'monkey -p com.netease.tom 1'])
print('monkey 已发 @', time.strftime('%H:%M:%S'))
dev = frida.get_device_manager().add_remote_device('127.0.0.1:45679')

# 0.5s 轮询 pid
pid = None
t0 = time.time()
while time.time() - t0 < 30:
    pid = get_pid()
    if pid:
        break
    time.sleep(0.5)
print('pid:', pid, '耗时 %.1fs' % (time.time() - t0))
if not pid:
    print('未找到进程'); sys.exit(1)

print('立即 attach (期望 <60s)...')
t1 = time.time()
session = dev.attach(pid)
print('attached! 耗时 %.1fs' % (time.time() - t1))
JS = open(r'C:\Users\20751\Desktop\猫和老鼠\ultimate_v3.py', encoding='utf-8').read().split('JS = r"""')[1].split('"""')[0]
script = session.create_script(JS)
script.on('message', lambda m, d: print('[msg]', m))
script.load()
print('v3 loaded! 保持 420s')
time.sleep(420)

if __name__ == '__main__':
    pass