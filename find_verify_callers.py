# -*- coding: utf-8 -*-
"""1) 找 bl 0xbc5e4c (X509_verify_cert) 的调用者
2) 宽松扫描 0xdebaa8 页 0xdeb000 的 adrp 引用者 (任何偏移)"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

# 1) bl 0xbc5e4c
tgt = 0xbc5e4c
callers = []
for lo, hi in [(0x0, 0x10022b8), (0x1574000, len(d)-4)]:
    for o in range(lo, hi-4, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFC000000) == 0x94000000:  # bl
            imm26 = w & 0x3FFFFFF
            if imm26 & 0x2000000: imm26 -= 0x4000000
            if o + (imm26 << 2) == tgt:
                callers.append(o)
print(f"[bl->0x{ tgt:x}] {len(callers)} 调用者: {[hex(c) for c in callers]}")

# 2) adrp -> 0xdeb000 页 (任何 add/ldr 偏移), ±0x1000 窗口
page = 0xdeb000
hits = []
for lo, hi in [(0x0, 0x10022b8), (0x1574000, len(d)-4)]:
    for o in range(lo, hi-4, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0x9F000000) == 0x90000000:
            rd = w & 0x1F
            immhi = (w >> 5) & 0x7FFFF
            immlo = (w >> 29) & 3
            imm = (immhi << 14) | (immlo << 12)
            if imm & 0x100000: imm -= 0x200000
            if ((o & ~0xFFF) + imm) == page:
                for j in range(o+4, min(o+0x1000, hi-4), 4):
                    w2 = struct.unpack_from('<I', d, j)[0]
                    if (w2 & 0x1F) != rd: continue
                    if (w2 & 0xFFC00000) == 0x91000000:  # add
                        hits.append((o, j, 'add', (w2 >> 10) & 0xFFF))
                    elif (w2 & 0xFFC00000) == 0xF9400000:  # ldr
                        hits.append((o, j, 'ldr', ((w2 >> 10) & 0xFFF) << 3))
# 去重 (adrp 相同只看首个 add/ldr) 并打印
seen = set()
for o, j, t, off in hits:
    if o in seen: continue
    seen.add(o)
    print(f"adrp@{o:#x} {t}@{j:#x} off={off:#x} -> va={page+off:#x}")
print(f"[adrp->0xdeb000] 共 {len(seen)} 个 adrp")

# 3) 顺带: 0xdebaa8 周边字符串确认
import re
seg = d[0xdeba40:0xdebb20]
for m in re.finditer(rb'[\x20-\x7e]{6,}', seg):
    s = m.group().decode()
    print(f"  0x{0xdeba40+m.start():#x}: '{s[:80]}'")