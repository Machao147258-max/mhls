# -*- coding: utf-8 -*-
# 提取: 每个 luac = 头到下一个头(含子函数/常量)
import json, struct, os

data = open(r'C:\Users\20751\tomdump\mega\all.bin', 'rb').read()
OUT = r'C:\Users\20751\tomdump\mega_luac'
os.makedirs(OUT, exist_ok=True)

HDR = b'\x1b\x4c\x75\x61\x51\x00'
heads = []
pos = 0
while True:
    i = data.find(HDR, pos)
    if i < 0: break
    pos = i + 1
    ln = struct.unpack_from('<I', data, i+12)[0]
    if not (0 < ln < 500): continue
    src = data[i+16:i+16+ln-1]
    if src.startswith(b'@src'):
        heads.append((i, src))
print(f'@src 块头: {len(heads)}')

seen = set()
for idx, (i, src) in enumerate(heads):
    # 块尾 = 下一个头
    end = heads[idx+1][0] if idx+1 < len(heads) else min(i + 3_000_000, len(data))
    key = (src, end - i)
    if key in seen: continue
    seen.add(key)
    name = src.decode('utf-8','replace').replace('/', '_').replace('@', '').strip()
    name = ''.join(c if c.isalnum() or c in '._-' else '_' for c in name)
    fn = os.path.join(OUT, f'{name}.luac')
    with open(fn, 'wb') as f:
        f.write(data[i:end])
    print(f'✓ {name} ({end-i}B)')
print(f'共 {len(seen)} 个')