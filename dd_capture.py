# -*- coding: utf-8 -*-
"""
dd_capture.py — 纯 /proc 定点抓取(零注入,无 frida)
用法: python dd_capture.py <PID> [outdir]
流程:
  1. adb 读 /proc/<PID>/maps, 按大小挑出候选 rw- 段(与 Lua 内存段特征相符: 2-32MB 整数幂大小)
  2. 逐段 dd if=/proc/<PID>/mem skip=... count=... 到 /data/local/tmp
  3. adb pull 到本地 outdir
  4. 本地扫 Lua5.1 头, 逐 chunk 解析长度, 拆出 .luac
  5. 打印可反编译的 chunk 清单
"""
import os, re, subprocess, sys, struct, glob, hashlib

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
LOCAL_OUT = sys.argv[2] if len(sys.argv) > 2 else r'C:\Users\20751\tomdump\dd_out'
DEV_OUT = '/data/local/tmp/tdd'
PID = sys.argv[1]

os.makedirs(LOCAL_OUT, exist_ok=True)

def sh(*a):
    r = subprocess.run([ADB] + list(a), capture_output=True, text=True, timeout=120)
    return r.stdout

# 1. maps
maps = sh('shell', 'su', '-c', f'cat /proc/{PID}/maps')
ranges = []
for line in maps.splitlines():
    m = re.match(r'([0-9a-f]+)-([0-9a-f]+)\s+(rw-\S)\s+[0-9a-f]+\s+\S+\s+\d+\s+(.*)', line)
    if not m:
        continue
    start = int(m.group(1), 16); end = int(m.group(2), 16)
    size = end - start
    path = m.group(4)
    # Lua 脚本缓冲的宿主: 空路径匿名段 + scudo 池(probe4 实证); jit/gralloc/文件映射是噪音
    if path == '' or path.startswith('[anon:scudo'):
        if 1 * 1024 * 1024 <= size <= 32 * 1024 * 1024:
            ranges.append((start, end, size, path))
ranges.sort(key=lambda r: -r[2])
print(f'空路径候选段 {len(ranges)} 个:')
for s, e, sz, p in ranges[:20]:
    print(f'  {s:#x}-{e:#x}  {sz/1048576:.1f}MB')

# 2. dd 抓取
for f in glob.glob(os.path.join(LOCAL_OUT, 'seg_*.bin')):
    os.remove(f)
sh('shell', 'su', '-c', f'rm -rf {DEV_OUT}; mkdir -p {DEV_OUT}')
pulled = []
for i, (s, e, sz, p) in enumerate(ranges[:40]):
    skip = s // 4096
    count = (sz + 4095) // 4096
    name = f'seg_{s:012x}_{sz // 1024}k'
    sh('shell', 'su', '-c', f'dd if=/proc/{PID}/mem bs=4096 skip={skip} count={count} of={DEV_OUT}/{name}.bin 2>/dev/null')
    sh('pull', f'{DEV_OUT}/{name}.bin', os.path.join(LOCAL_OUT, name + '.bin'))
    pulled.append(os.path.join(LOCAL_OUT, name + '.bin'))
print(f'已抓取 {len(pulled)} 段')

# 3. 本地扫 chunk
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import extract_chunks as ec

allchunks = []
for fn in pulled:
    if not os.path.exists(fn):
        continue
    data = open(fn, 'rb').read()
    cs = ec.scan_chunks(data)
    if cs:
        print(f'\n{os.path.basename(fn)}: {len(cs)} chunk')
        for name, off, end in cs:
            print(f'    {name}  size={end-off}')
            allchunks.append((fn, name, off, end))

# 4. 拆 .luac
os.makedirs(os.path.join(LOCAL_OUT, 'luac'), exist_ok=True)
n = 0
for fn, name, off, end in allchunks:
    data = open(fn, 'rb').read()
    safe = (name or 'chunk').replace('/', '__').replace('@', '').replace('\\', '__')
    safe = ''.join(c for c in safe if c.isalnum() or c in '._-')[:80]
    out = os.path.join(LOCAL_OUT, 'luac', f'{n:04d}_{safe}.luac')
    with open(out, 'wb') as f:
        f.write(data[off:end])
    n += 1
print(f'\n共拆出 {n} 个 .luac → {os.path.join(LOCAL_OUT, "luac")}')