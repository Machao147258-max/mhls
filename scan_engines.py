# -*- coding: utf-8 -*-
# 扫描 tom 进程引擎库
import subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
DEV = '127.0.0.1:7555'

def sh(cmd):
    r = subprocess.run([ADB, '-s', DEV, 'shell', cmd], capture_output=True, text=True, timeout=30)
    return r.stdout

# 1. tom 进程
print('=== tom 进程 ===')
ps = sh("su -c 'ps -A | grep netease.tom'")
print(ps)

# 2. pids
pids = []
for line in ps.splitlines():
    parts = line.split()
    if len(parts) > 1 and parts[1].isdigit():
        pids.append(parts[1])
print('pids:', pids)

# 3. 引擎扫描
for p in pids:
    print(f'\n=== PID={p} ===')
    maps = sh(f'su -c "cat /proc/{p}/maps 2>/dev/null"')
    so = set()
    for m in maps.splitlines():
        if '.so' in m:
            name = m.split('/')[-1]
            if any(k in name.lower() for k in ['cocos', 'lua', 'sec', 'unisec', 'engine', 'game', 'tom', 'tcb', 'chano', 'hp1', 'ngmod']):
                so.add(name)
    for s in sorted(so)[:25]:
        print('  ', s)
    if not so:
        print('  (无游戏库)')