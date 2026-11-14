# -*- coding: utf-8 -*-
"""round_capture.py — 多轮 dd 抓取 + 合并
用法: python round_capture.py <PID> [轮数]
"""
import os, sys, time, glob, shutil, re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dd_capture as dc
import extract_chunks as ec

PID = sys.argv[1]
ROUNDS = int(sys.argv[2]) if len(sys.argv) > 2 else 3
BASE = dc.LOCAL_OUT
MERGED = os.path.join(BASE, 'merged')

def one_round(r):
    outdir = os.path.join(BASE, f'round{r}')
    os.makedirs(outdir, exist_ok=True)
    # 复用 dd_capture 的抓取,但输出到 round 目录
    maps = dc.sh('shell', 'su', '-c', f'cat /proc/{PID}/maps')
    ranges = []
    for line in maps.splitlines():
        m = re.match(r'([0-9a-f]+)-([0-9a-f]+)\s+(rw-\S)\s+[0-9a-f]+\s+\S+\s+\d+\s*(.*)', line)
        if not m:
            continue
        start = int(m.group(1), 16); end = int(m.group(2), 16)
        size = end - start
        path = m.group(4)
        if (path == '' or path.startswith('[anon:scudo')) and 1 * 1024 * 1024 <= size <= 32 * 1024 * 1024:
            ranges.append((start, end, size))
    dev = f'/data/local/tmp/tdd{r}'
    dc.sh('shell', 'su', '-c', f'rm -rf {dev}; mkdir -p {dev}')
    n = 0
    for start, end, size in ranges:
        skip = start // 4096
        count = (size + 4095) // 4096
        name = f'seg_{start:012x}_{size // 1024}k'
        dc.sh('shell', 'su', '-c', f'dd if=/proc/{PID}/mem bs=4096 skip={skip} count={count} of={dev}/{name}.bin 2>/dev/null')
        dc.sh('pull', f'{dev}/{name}.bin', os.path.join(outdir, name + '.bin'))
        n += 1
    # 本地扫 chunk 并拆 luac
    luac_dir = os.path.join(outdir, 'luac')
    os.makedirs(luac_dir, exist_ok=True)
    cnt = 0
    for f in glob.glob(os.path.join(outdir, 'seg_*.bin')):
        d = open(f, 'rb').read()
        for name, off, end in ec.scan_chunks(d):
            safe = (name or 'chunk').replace('/', '__').replace('@', '').replace('\\', '__')
            safe = ''.join(c for c in safe if c.isalnum() or c in '._-')[:90]
            out = os.path.join(luac_dir, f'{cnt:05d}_{safe}.luac')
            with open(out, 'wb') as fo:
                fo.write(d[off:end])
            cnt += 1
    print(f'[round{r}] 段 {n} 个, 拆出 {cnt} 个 chunk')
    return cnt

total = 0
for r in range(1, ROUNDS + 1):
    try:
        total += one_round(r)
    except Exception as e:
        print(f'[round{r}] 失败: {e}')
    if r < ROUNDS:
        print(f'-- 等待 60 秒进下一轮 --')
        time.sleep(60)

print(f'\n三轮共拆出 {total} 个 chunk')
# 按名字去重合并
os.makedirs(MERGED, exist_ok=True)
seen = {}
for f in glob.glob(os.path.join(BASE, 'round*', 'luac', '*.luac')):
    name = os.path.basename(f)
    # 取名字段(00001_@src_...)
    key = name.split('_', 1)[-1] if '_' in name else name
    d = open(f, 'rb').read()
    if key not in seen or len(d) > len(seen[key]):
        seen[key] = d
with open(os.path.join(MERGED, 'index.txt'), 'w') as f:
    for k in sorted(seen):
        f.write(k + '\n')
for i, (k, d) in enumerate(seen.items()):
    with open(os.path.join(MERGED, f'{i:04d}_{k}'), 'wb') as f:
        f.write(d)
print(f'合并去重后: {len(seen)} 个唯一脚本')