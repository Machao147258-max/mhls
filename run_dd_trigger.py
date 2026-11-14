# -*- coding: utf-8 -*-
# 触发+dd抓取: 切前后台触发 → dd 抓 X1V5fzTo 段 + 堆 → 找新 16B 串 (零注入)
import subprocess, time, os, re, struct

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUT = r'C:\Users\20751\tomdump\dd_trigger_out.txt'
CYCLES = 5

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

os.makedirs(r'C:\Users\20751\tomdump\dd_trig', exist_ok=True)
KEY1 = bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b')

def grab(pid, s, e, name):
    page, n = s >> 12, (e - s + 4095) >> 12
    dev = f'/data/local/tmp/dt_{name}.bin'
    sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={n} of={dev} 2>&1"'], t=60)
    sh(['pull', dev, rf'C:\Users\20751\tomdump\dd_trig\{name}.bin'], t=60)

log(f'=== 触发+dd {time.strftime("%H:%M:%S")} ===')
for cyc in range(1, CYCLES + 1):
    log(f'--- 轮 {cyc} ---')
    pid = sh(['shell', 'pidof com.netease.tom'])
    if not pid.isdigit():
        log('  游戏未运行')
        continue
    # 触发: 切后台回前台
    sh(['shell', 'input keyevent 3'])
    time.sleep(3)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    time.sleep(3)
    # 立即抓 X1V5fzTo 段 + 小堆
    grab(pid, 0x778eba697000, 0x778eba7d7000, f'c{cyc}_x1')
    grab(pid, 0x778e31376000, 0x778e329a5000, f'c{cyc}_h22')
    # 分析
    x1 = open(rf'C:\Users\20751\tomdump\dd_trig\c{cyc}_x1.bin', 'rb').read()
    h22 = open(rf'C:\Users\20751\tomdump\dd_trig\c{cyc}_h22.bin', 'rb').read()
    nx = x1.count(b'X1V5fzTo')
    nl = x1.count(b'\x1bLuaQ')
    k1 = h22.find(KEY1)
    # 16B 可打印串
    cands = set()
    for m in re.finditer(rb'[\x20-\x7e]{16}', h22):
        s16 = m.group(0)[:16]
        if re.match(rb'^[A-Za-z0-9_.\-]{16}$', s16) and s16[:4].lower() not in (b'com/', b'org/', b'java'):
            cands.add(s16)
    log(f'  x1段: X1={nx} luac={nl} | 堆22: KEY1={hex(k1) if k1>=0 else "NO"} 16B串={len(cands)}')
    with open(rf'C:\Users\20751\tomdump\dd_trig\c{cyc}_cands.txt', 'w') as f:
        for c in sorted(cands):
            f.write(c.decode() + '\n')
    # 游戏状态
    alive = sh(['shell', 'pidof com.netease.tom']).isdigit()
    log(f'  游戏存活: {alive}')
    time.sleep(10)
log('=== 结束 ===')
logf.close()
