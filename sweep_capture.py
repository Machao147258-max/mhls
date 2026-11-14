# -*- coding: utf-8 -*-
"""sweep_capture.py — 长程多次快照抓取
用法: python sweep_capture.py <PID> [轮数] [间隔秒]
每轮: 全段 dd(一次 su) → pull → 提取 chunk → 去重合并
"""
import os, sys, re, glob, subprocess, time, json, base64

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
PID = sys.argv[1]
ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 12
INTERVAL = int(sys.argv[3]) if len(sys.argv) > 3 else 90
BASE = os.path.join(r'C:\Users\20751\tomdump', f'sweep_{PID}')
MERGED = os.path.join(BASE, 'merged')
os.makedirs(MERGED, exist_ok=True)

def sh(*a, t=900):
    r = subprocess.run([ADB] + list(a), capture_output=True, text=True, timeout=t)
    return r.stdout

def one_round(r):
    outdir = os.path.join(BASE, f'r{r}')
    os.makedirs(outdir, exist_ok=True)
    for f in glob.glob(os.path.join(outdir, 's*.bin')):
        os.remove(f)
    maps = sh('shell', 'su', '-c', f'cat /proc/{PID}/maps')
    ranges = []
    for line in maps.splitlines():
        m = re.match(r'([0-9a-f]+)-([0-9a-f]+)\s+(rw-\S)\s+[0-9a-f]+\s+\S+\s+\d+\s*(.*)', line)
        if not m: continue
        size = int(m.group(2), 16) - int(m.group(1), 16)
        path = m.group(4)
        if (path == '' or path.startswith('[anon')) and 128 * 1024 <= size <= 32 * 1024 * 1024:
            ranges.append((int(m.group(1), 16), int(m.group(2), 16), size))
    json.dump(ranges, open(os.path.join(outdir, 'segmap.json'), 'w'))
    dev = f'/data/local/tmp/sw{r}'
    script = '#!/system/bin/sh\n' + f'mkdir -p {dev}\n'
    for i, (s, e, sz) in enumerate(ranges):
        script += f'dd if=/proc/{PID}/mem bs=4096 skip={s//4096} count={(e-s+4095)//4096} of={dev}/s{i:03d}.bin 2>/dev/null\n'
    script += f'echo DONE {len(ranges)}\n'
    with open(os.path.join(outdir, 'cap.sh'), 'wb') as f:
        f.write(script.encode())
    sh('push', os.path.join(outdir, 'cap.sh'), '/data/local/tmp/caprun.sh')
    out = sh('shell', 'su', '-c', 'sh /data/local/tmp/caprun.sh')
    n = 0
    for i in range(len(ranges)):
        name = f's{i:03d}.bin'
        sh('pull', f'{dev}/{name}', os.path.join(outdir, name), t=120)
        n += 1
    # 提取
    import extract_chunks as ec
    cnt = 0
    for f in glob.glob(os.path.join(outdir, 's*.bin')):
        d = open(f, 'rb').read()
        for nm, off, end in ec.scan_chunks(d):
            safe = (nm or 'chunk').replace('/', '__').replace('@', '').replace('\\', '__')
            safe = ''.join(c for c in safe if c.isalnum() or c in '._-')[:90]
            with open(os.path.join(outdir, f'{cnt:05d}_{safe}.luac'), 'wb') as fo:
                fo.write(d[off:end])
            cnt += 1
    print(f'[r{r}] {len(ranges)} 段, {cnt} chunk', flush=True)
    return cnt

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
total = 0
for r in range(1, ROUNDS + 1):
    try:
        total += one_round(r)
    except Exception as e:
        print(f'[r{r}] 失败: {e}', flush=True)
    if r < ROUNDS:
        time.sleep(INTERVAL)
print(f'完成, 共 {total} chunk')

# 合并去重
seen = {}
for f in glob.glob(os.path.join(BASE, 'r*', '*.luac')):
    d = open(f, 'rb').read()
    nm = os.path.basename(f).split('_', 1)[-1]
    if nm not in seen or len(d) > len(seen[nm]):
        seen[nm] = d
for i, (nm, d) in enumerate(seen.items()):
    with open(os.path.join(MERGED, f'{i:04d}_{nm}'), 'wb') as f:
        f.write(d)
print(f'合并去重: {len(seen)} 个唯一脚本 → {MERGED}')