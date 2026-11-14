# -*- coding: utf-8 -*-
# 启动 + 观察游戏稳定性: 每 10 秒记录 pid/so/前台, 90 秒
import subprocess, time

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUT = r'C:\Users\20751\tomdump\observe_game.txt'

def sh(args, t=20):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return f'ERR {e}'

logf = open(OUT, 'a', encoding='utf-8')
def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    logf.write(s + '\n'); logf.flush()

log(f'=== 观察 {time.strftime("%H:%M:%S")} ===')
sh(['shell', 'am force-stop com.netease.tom'])
time.sleep(2)
sh(['shell', 'monkey -p com.netease.tom 1'])
for i in range(9):
    time.sleep(10)
    pid = sh(['shell', 'pidof com.netease.tom'])
    so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos']) if pid else '0'
    fg = sh(['shell', 'dumpsys activity activities | grep topResumedActivity | head -1'])[:90]
    log(f'[{i*10+10}s] pid={pid} so={so} fg={fg}')
    if not pid:
        log('  [!!] 游戏死亡')
        break
log('=== 观察结束 ===')
logf.close()
