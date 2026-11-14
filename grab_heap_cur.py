# -*- coding: utf-8 -*-
# 抓当前实例所有大 rw 段 (堆) — 供滑窗验证
import subprocess, time, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUTD = r'C:\Users\20751\tomdump\heap_cur'
os.makedirs(OUTD, exist_ok=True)

def sh(args, t=120):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return f'ERR {e}'

pid = sh(['shell', 'pidof com.netease.tom'])
print('pid:', pid, flush=True)
if not pid.isdigit():
    raise SystemExit('无游戏')
maps = sh(['shell', f'cat /proc/{pid}/maps'])
segs = []
for l in maps.splitlines():
    p = l.split()
    if len(p) < 2: continue
    s, e = p[0].split('-')
    s, e = int(s, 16), int(e, 16)
    if 'rw' in p[1] and 0x700000000000 <= s <= 0x800000000000 and e - s >= 0x200000:
        segs.append((s, e))
print(f'{len(segs)} 个大 rw 段', flush=True)
for s, e in segs:
    name = f'{s & 0xffffffffff:x}'
    page, cnt = s >> 12, (e - s + 4095) >> 12
    if cnt > 0x8000000:  # >32GB 跳过
        continue
    dev = f'/data/local/tmp/hc_{name}.bin'
    sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={cnt} of={dev} 2>&1"'], t=300)
    sh(['pull', dev, rf'{OUTD}\{name}.bin'], t=300)
    b = open(rf'{OUTD}\{name}.bin', 'rb').read()
    nz = sum(1 for x in b[:65536] if x)
    print(f'{hex(s)}: {len(b)//1048576}MB 非零64KB={nz}', flush=True)
print('=== 完成 ===', flush=True)
