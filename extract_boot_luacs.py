# -*- coding: utf-8 -*-
# 从 dd_live_1973 / sweep_1973 提取全部 luac 并识别 source 名
import os, struct, glob

def extract_luacs(path):
    """提取文件中所有 luac, 返回 [(offset, data, srcname)]"""
    try:
        data = open(path, 'rb').read()
    except Exception:
        return []
    out = []
    pos = 0
    while True:
        i = data.find(b'\x1bLua', pos)
        if i < 0:
            break
        # 验证 Lua 5.1: 1b 4c 75 61 51 00 01
        if i + 7 <= len(data) and data[i+4:i+7] == b'Q\x00\x01':
            try:
                ln = struct.unpack_from('<I', data, i + 12)[0]
                if 0 < ln < 4096:
                    src = data[i+16:i+16+ln-1]
                    srcname = src.decode('utf-8', 'replace')
                    out.append((i, srcname))
            except Exception:
                pass
        pos = i + 1
    return out

dirs = [r'C:\Users\20751\tomdump\dd_live_1973', r'C:\Users\20751\tomdump\sweep_1973\r1', r'C:\Users\20751\tomdump\sweep_1973\r2', r'C:\Users\20751\tomdump\sweep_1973\r3']
allhits = {}
for d in dirs:
    if not os.path.isdir(d):
        continue
    for f in os.listdir(d):
        p = os.path.join(d, f)
        hits = extract_luacs(p)
        if hits:
            allhits[p] = hits
print('=== 启动早期 dump 中的 luac ===')
names = set()
for p, hits in sorted(allhits.items()):
    for off, src in hits:
        names.add(src)
        print(f'{os.path.basename(p)} @ {off:#x}: {src}')
print()
print('=== 唯一 source 名 (%d) ===' % len(names))
for n in sorted(names):
    print('  ', n)
