# -*- coding: utf-8 -*-
# opcode 行为聚类: 统计每个 opcode 的 B/C 值域分布
import struct, glob, os
from collections import Counter, defaultdict

SO = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so','rb').read()
FMT = SO[0xcd3820:0xcd3820+42]

stats = defaultdict(lambda: Counter())
tot = Counter()
for f in glob.glob(r'C:\Users\20751\tomdump\mega_luac\*.luac'):
    b = open(f, 'rb').read()
    # 快速: 从第一个 @src 块找 code (简化: 直接扫所有 32 位指令样本)
    # 用已知块: 找 @src 头后
    pos = 0
    while True:
        i = b.find(b'\x1bLuaQ\x00', pos)
        if i < 0: break
        pos = i + 1
        ln = struct.unpack_from('<I', b, i+12)[0]
        if not (0 < ln < 500): continue
        p = i + 16 + ln + 12
        if p + 4 > len(b): continue
        sc = struct.unpack_from('<I', b, p)[0]
        if not (0 < sc < 0x100000): continue
        p += 4
        code = b[p:p+sc*4]
        for j in range(0, len(code)-3, 4):
            v = struct.unpack_from('<I', code, j)[0]
            if v == 0: continue  # 跳过 0 填充
            op = v & 0x3F
            if op >= 42: continue
            a = (v >> 6) & 0xFF
            b2 = (v >> 14) & 0x1FF
            c = (v >> 23) & 0x1FF
            bx = (v >> 14) & 0x3FFFF
            stats[op]['n'] += 1
            tot[op] += 1
            if b2 < 256: stats[op]['b_reg'] += 1
            else: stats[op]['b_k'] += 1
            if c == 0: stats[op]['c0'] += 1
            else: stats[op]['cN'] += 1
            stats[op]['bmax'] = max(stats[op]['bmax'], b2)
            stats[op]['amax'] = max(stats[op]['amax'], a)
            stats[op]['bxmax'] = max(stats[op]['bxmax'], bx)
        break  # 只取第一个块(主块)

print(f'{"op":>3} {"fmt":>4} {"总数":>7} {"B<256":>7} {"B>=256":>8} {"C=0":>6} {"C>0":>6} {"Bmax":>6} {"Amax":>6} {"Bxmax":>7}')
for op in range(42):
    s = stats[op]
    if s['n'] == 0:
        print(f'{op:3d} {FMT[op]:#4x} {"-":>7}')
        continue
    print(f'{op:3d} {FMT[op]:#4x} {s["n"]:7d} {s["b_reg"]:7d} {s["b_k"]:8d} {s["c0"]:6d} {s["cN"]:6d} {s["bmax"]:6d} {s["amax"]:6d} {s["bxmax"]:7d}')