# -*- coding: utf-8 -*-
"""scan_x1v5.py — 扫进程内存找 X1V5fzTo 密文 (和可能的 luac 明文)
用法: python scan_x1v5.py <PID>
"""
import os, sys, re, subprocess, json

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
PID = sys.argv[1]
OUT = r'C:\Users\20751\Desktop\猫和老鼠\tom_scan'
os.makedirs(OUT, exist_ok=True)

def sh(*a, t=600):
    r = subprocess.run([ADB] + list(a), capture_output=True, text=True, timeout=t)
    return r.stdout

maps = sh('shell', 'su', '-c', f'cat /proc/{PID}/maps')
ranges = []
for line in maps.splitlines():
    m = re.match(r'([0-9a-f]+)-([0-9a-f]+)\s+(\S+)\s+[0-9a-f]+\s+\S+\s+\d+\s*(.*)', line)
    if not m:
        continue
    start, end = int(m.group(1), 16), int(m.group(2), 16)
    perm, path = m.group(3), m.group(4)
    size = end - start
    # rw 匿名段 + 可读文件段 (排除系统)
    if 'r' in perm and ('w' in perm or path == '' or 'tom' in path):
        if 64 * 1024 <= size <= 64 * 1024 * 1024:
            ranges.append((start, end, size))
print(f'候选段: {len(ranges)}')

# 逐个 dd 读取并 grep X1V5fzTo
found = []
for i, (start, end, size) in enumerate(ranges):
    skip = start
    # 用 dd 读到 PC (一次 4MB 上限, 分段)
    dev = f'/data/local/tmp/sc{PID}'
    r = sh('shell', 'su', '-c', f'dd if=/proc/{PID}/mem bs=1M skip={skip // (1024*1024)} count={size // (1024*1024) + 1} 2>/dev/null | grep -abo "X1V5fzTo" | head -5')
    if r.strip():
        found.append((start, end, r.strip()))
        print(f'  HIT seg {start:#x}-{end:#x}: {r.strip()[:200]}')

print(f'共 {len(found)} 段含 X1V5fzTo')
json.dump(found, open(os.path.join(OUT, f'hits_{PID}.json'), 'w'), indent=1)
