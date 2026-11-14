# -*- coding: utf-8 -*-
"""min_capture.py — 单次 su 调用的最小痕迹抓取
用法: python min_capture.py <PID>
"""
import os, sys, re, glob, subprocess, time, json

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
PID = sys.argv[1]
OUT = os.path.join(r'C:\Users\20751\tomdump', f'dd_live_{PID}')
DEV = f'/data/local/tmp/cap{PID}'
os.makedirs(OUT, exist_ok=True)

def sh(*a, t=300):
    r = subprocess.run([ADB] + list(a), capture_output=True, text=True, timeout=t)
    return r.stdout

# 1. maps
maps = sh('shell', 'su', '-c', f'cat /proc/{PID}/maps')
ranges = []
for line in maps.splitlines():
    m = re.match(r'([0-9a-f]+)-([0-9a-f]+)\s+(rw-\S)\s+[0-9a-f]+\s+\S+\s+\d+\s*(.*)', line)
    if not m:
        continue
    start = int(m.group(1), 16); end = int(m.group(2), 16)
    size = end - start
    path = m.group(4)
    if (path == '' or path.startswith('[anon')) and 128 * 1024 <= size <= 32 * 1024 * 1024:
        ranges.append((start, end, size))
print(f'候选段: {len(ranges)}')

# 1.5 落盘段映射(保证 s{i} ↔ segmap[i] 一致)
os.makedirs(OUT, exist_ok=True)
json.dump(ranges, open(os.path.join(OUT, 'segmap.json'), 'w'))
# 清设备旧文件
sh('shell', 'su', '-c', f'rm -rf {DEV}; mkdir -p {DEV}')
# 2. 生成单个 shell 脚本 → adb push → 一次 su 执行所有 dd
script = '#!/system/bin/sh\n'
script += f'mkdir -p {DEV}\n'
for i, (start, end, size) in enumerate(ranges):
    skip = start // 4096
    count = (size + 4095) // 4096
    script += f'dd if=/proc/{PID}/mem bs=4096 skip={skip} count={count} of={DEV}/s{i:03d}.bin 2>/dev/null\n'
script += f'echo DONE {len(ranges)}\n'
local_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'caprun.sh')
with open(local_script, 'wb') as f:
    f.write(script.encode('utf-8'))   # 二进制写, 保持 LF, 避免 CRLF 被 Android sh 误读
sh('push', local_script, '/data/local/tmp/caprun.sh')
out = sh('shell', 'su', '-c', 'sh /data/local/tmp/caprun.sh')
print('执行结果:', out.strip()[:200])

# 3. pull(此 adb 不支持多文件 pull,逐个拉)
os.makedirs(OUT, exist_ok=True)
for f in glob.glob(os.path.join(OUT, 's*.bin')):
    os.remove(f)   # 清本地旧文件,保证 s{i} ↔ segmap[i] 一致
import glob as _g
have = set(os.path.basename(f) for f in _g.glob(os.path.join(OUT, 's*.bin')))
n = 0
for j in range(len(ranges)):
    name = f's{j:03d}.bin'
    if name in have:
        continue
    r = sh('pull', f'{DEV}/{name}', os.path.join(OUT, name), t=120)
    n += 1
print(f'已 pull {n} 个 → {OUT}')

# 4. 本地解析
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_chunks as ec
luac = os.path.join(OUT, 'luac')
os.makedirs(luac, exist_ok=True)
cnt = 0
for f in glob.glob(os.path.join(OUT, 's*.bin')):
    d = open(f, 'rb').read()
    for name, off, end in ec.scan_chunks(d):
        safe = (name or 'chunk').replace('/', '__').replace('@', '').replace('\\', '__')
        safe = ''.join(c for c in safe if c.isalnum() or c in '._-')[:90]
        with open(os.path.join(luac, f'{cnt:05d}_{safe}.luac'), 'wb') as fo:
            fo.write(d[off:end])
        cnt += 1
print(f'共拆出 {cnt} 个 chunk')