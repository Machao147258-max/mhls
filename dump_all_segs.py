# -*- coding: utf-8 -*-
# 全量抓取剩余 rw 段(排除已抓), 搜 Lua TString 特征定位 Lua 堆
import subprocess, os, struct, glob

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
ALREADY = ['heap192', 'heap32', 'heap27', 'heap26', 'heap22', 'heap18', 'so_code1', 'so_code2', 'sodata']

def sh(args, t=60):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return f'ERR {e}'

pid = sh(['shell', 'pidof com.netease.tom'])
if not pid.isdigit():
    print('游戏未运行, 启动...')
    sh(['shell', 'monkey -p com.netease.tom 1'])
    for _ in range(60):
        import time
        time.sleep(1)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit(): break
print(f'PID={pid}')
# 等 so 加载 + 60s 让脚本加载
import time
for _ in range(60):
    so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
    if so.isdigit() and int(so) > 0: break
    time.sleep(1)
print('so 加载, 等 60s 脚本加载...')
time.sleep(60)

out = sh(['shell', f'su -c "cat /proc/{pid}/maps"'])
segs = []
for l in out.splitlines():
    p = l.split()
    if len(p) < 2: continue
    try:
        s, e = p[0].split('-'); s, e = int(s, 16), int(e, 16)
    except: continue
    if 'rw' not in p[1]: continue
    if p[2] != '00000000': continue  # 匿名
    if e - s < 256 * 1024: continue
    if s < 0x700000000000 and not (0x2000000 <= s < 0xe000000): continue  # 用户区
    segs.append((s, e))
print(f'待抓段 {len(segs)}', flush=True)

os.makedirs(r'C:\Users\20751\tomdump\all_segs', exist_ok=True)
for idx, (s, e) in enumerate(segs):
    name = f'seg_{idx:03d}'
    page, n = s >> 12, (e - s + 4095) >> 12
    dev = f'/data/local/tmp/{name}.bin'
    r = sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={n} of={dev} 2>&1"'], t=300)
    sh(['pull', dev, rf'C:\Users\20751\tomdump\all_segs\{name}.bin'], t=300)
    b = open(rf'C:\Users\20751\tomdump\all_segs\{name}.bin', 'rb').read()
    # 搜 Lua TString 特征: len=8 (require) 或 len=16, 前有 hash
    marks = []
    for ln in (8, 16, 17):
        pat = struct.pack('<Q', ln)
        if pat in b: marks.append(f'len{ln}')
    n_x = b.count(b'X1V5fzTo')
    n_l = b.count(b'\x1bLuaQ')
    if marks or n_x or n_l:
        print(f'{name}: {hex(s)}-{hex(e)} {len(b)}B {marks} X1={n_x} luac={n_l}', flush=True)
print('完成', flush=True)
