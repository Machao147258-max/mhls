# -*- coding: utf-8 -*-
# 快速路径: 重启游戏 → 5s 轮询 → so 加载后立刻读槽(每 5s 直到有值)
import subprocess, time, sys

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUT = r'C:\Users\20751\tomdump\slot_read'
import os
os.makedirs(OUT, exist_ok=True)

def sh(args, t=20):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return ''

def logw(s):
    print(s, flush=True)
    with open(os.path.join(OUT, 'fast.log'), 'a') as f:
        f.write(s + '\n')

# 重启
sh(['shell', 'su -c am force-stop com.netease.tom'])
time.sleep(3)
sh(['shell', 'monkey -p com.netease.tom 1'])
logw('已重启游戏 @ %s' % time.strftime('%H:%M:%S'))

start = time.time()
last_pid = None
base = None
while time.time() - start < 300:
    p = sh(['shell', 'su -c pidof com.netease.tom']).strip()
    pid = p.split()[0] if p else None
    if pid and pid != last_pid:
        logw('[%ds] pid=%s' % (int(time.time() - start), pid))
        last_pid = pid
        base = None
    if pid:
        if not base:
            m = sh(['shell', 'su -c cat /proc/%s/maps | grep libcocos2dlua' % pid])
            for l in m.splitlines():
                if 'r--p' in l:
                    base = l.split('-')[0]
                    logw('[%ds] ★ so 加载! base=%s' % (int(time.time() - start), base))
                    break
        if base:
            # 读槽 (每 5s)
            slot = '%x' % (int(base, 16) + 0xff6cc50)
            v = sh(['shell', 'su -c "dd if=/proc/%s/mem bs=1 skip=$((0x%s)) count=8 2>/dev/null | xxd -p"' % (pid, slot)], t=30)
            v = v.replace('\n', '').strip()
            if v and v != '00' * 8 and len(v) >= 16:
                logw('[%ds] ★★ 槽值: %s' % (int(time.time() - start), v))
                ptr = int(v, 16)
                logw('单例: %#x' % ptr)
                for off in (0, 8, 0x10, 0x18, 0x20, 0x28, 0x30, 0x38, 0x40, 0x48, 0x50, 0x58, 0x60):
                    av = sh(['shell', 'su -c "dd if=/proc/%s/mem bs=1 skip=$((0x%x)) count=16 2>/dev/null | xxd -p"' % (pid, ptr + off)], t=30)
                    logw('  单例+%#x: %s' % (off, av.replace('\n', '').strip()))
                # 槽附近 0x100
                for off in range(0, 0x100, 0x10):
                    av = sh(['shell', 'su -c "dd if=/proc/%s/mem bs=1 skip=$((0x%x)) count=16 2>/dev/null | xxd -p"' % (pid, int(base, 16) + 0xff6cc00 + off)], t=30)
                    logw('  so+%#x: %s' % (0xff6cc00 + off, av.replace('\n', '').strip()))
                logw('DONE')
                sys.exit(0)
            else:
                logw('[%ds] 槽: %s (等待解密)' % (int(time.time() - start), v if v else '读失败'))
    else:
        logw('[%ds] 无进程' % int(time.time() - start))
    time.sleep(5)
logw('超时')
