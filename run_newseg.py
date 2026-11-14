# -*- coding: utf-8 -*-
# 启动后新段抓取: 记录启动前 maps → 启动 → 30s 后对比新段 → 抓新段分析
import subprocess, time, os, re, struct

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUT = r'C:\Users\20751\tomdump\newseg_out.txt'
ROUNDS = 3

def sh(args, t=30):
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

os.makedirs(r'C:\Users\20751\tomdump\newsegs', exist_ok=True)

def anon_segs(pid):
    out = sh(['shell', f'su -c "cat /proc/{pid}/maps 2>/dev/null"'])
    segs = set()
    for l in out.splitlines():
        p = l.split()
        if len(p) < 2: continue
        try:
            s, e = p[0].split('-'); s, e = int(s, 16), int(e, 16)
        except: continue
        if 'rw' not in p[1]: continue
        if p[2] != '00000000': continue
        if e - s < 0x10000: continue
        if not (0x700000000000 <= s <= 0x800000000000): continue
        segs.add((s, e))
    return segs

def grab(pid, s, e, name):
    page, n = s >> 12, (e - s + 4095) >> 12
    dev = f'/data/local/tmp/ns_{name}.bin'
    sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={n} of={dev} 2>&1"'], t=120)
    sh(['pull', dev, rf'C:\Users\20751\tomdump\newsegs\{name}.bin'], t=120)

KEY1 = bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b')
log(f'=== 新段抓取 {time.strftime("%H:%M:%S")} ===')
for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    # 启动前: 记录基线段
    old = anon_segs('')  # 无进程时可能失败
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    # 基线: 用已存在进程? 用空进程对照不行; 用启动后 3s 的段作为基线
    sh(['shell', 'monkey -p com.netease.tom 1'])
    pid = None
    for _ in range(30):
        time.sleep(1)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit(): break
    if not pid.isdigit():
        log('  启动失败')
        continue
    # 等 so 加载
    for _ in range(30):
        so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
        if so.isdigit() and int(so) > 0: break
        time.sleep(1)
    # 基线 = so 加载时刻的段
    base = anon_segs(pid)
    # 等 25s (解密/加载发生)
    time.sleep(25)
    now = anon_segs(pid)
    news = [x for x in now if x not in base]
    log(f'  新段 {len(news)} 个 (基线 {len(base)} → 现在 {len(now)})')
    for s, e in sorted(news, key=lambda x: -(x[1]-x[0]))[:8]:
        sz = e - s
        if sz > 64 * 1024 * 1024:  # 跳过巨大段
            log(f'    {hex(s)}-{hex(e)} {sz//1048576}MB (跳过)')
            continue
        name = f'r{rnd}_{s & 0xfffff:x}'
        try:
            grab(pid, s, e, name)
            b = open(rf'C:\Users\20751\tomdump\newsegs\{name}.bin', 'rb').read()
            nx = b.count(b'X1V5fzTo')
            nl = b.count(b'\x1bLuaQ')
            k1 = b.find(KEY1)
            print(f'    {hex(s)}-{hex(e)} {sz//1024}KB X1={nx} luac={nl} KEY1={hex(k1) if k1>=0 else "NO"}', flush=True)
            logf.write(f'    {hex(s)}-{hex(e)} {sz//1024}KB X1={nx} luac={nl} KEY1={hex(k1) if k1>=0 else "NO"}\n'); logf.flush()
        except Exception as ex:
            log(f'    {hex(s)} 抓取失败 {ex}')
    logf.flush()
log('=== 结束 ===')
logf.close()
