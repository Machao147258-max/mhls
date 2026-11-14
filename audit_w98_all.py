# -*- coding: utf-8 -*-
"""1) 完整反汇编 0x8dce00~0x8dd800 (游戏 SSL_CTX 配置函数), 标注 bl 目标
2) 扫描 bl -> 0xc8b7f8 (0xf 分发 setter) 的调用者
3) 全局扫描 str x?, [x?, #0x98] (rn 任意, 非 sp) 所有写入点"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
CODE_END = 0x10022b8

# bl 目标标注
def bl_target(addr):
    w = struct.unpack_from('<I', d, addr)[0]
    if (w & 0xFC000000) == 0x94000000:
        imm26 = w & 0x3FFFFFF
        if imm26 & 0x2000000: imm26 -= 0x4000000
        return (addr + (imm26 << 2)) & 0xFFFFFFFF
    return None

print("=== 1) 0x8dce00~0x8dd800 (SSL_CTX 配置) ===")
for ins in md.disasm(d[0x8dce00:0x8dd800], 0x8dce00):
    if ins.mnemonic == 'bl':
        t = bl_target(ins.address)
        print(f"  {ins.address:#x}: bl {t:#x}")
    else:
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== 2) bl -> 0xc8b7f8 调用者 ===")
hits = []
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFC000000) == 0x94000000:
        imm26 = w & 0x3FFFFFF
        if imm26 & 0x2000000: imm26 -= 0x4000000
        t = (o + (imm26 << 2)) & 0xFFFFFFFF
        if t in (0xc8b7f8, 0xc8b9b0, 0xc8b838):
            hits.append((o, t))
for h in hits:
    print(f"  {h[0]:#x} -> {h[1]:#x}")

print("\n=== 3) 全局 str x?, [x?, #0x98] 写入点 (rn != 31) ===")
w98 = []
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0xF9000000:
        imm = ((w >> 10) & 0xFFF) << 3
        rn = (w >> 5) & 0x1F
        rt = w & 0x1F
        if imm == 0x98 and rn != 31:
            w98.append((o, rn, rt))
print(f"  {len(w98)} 处")
from collections import Counter
bases = Counter(rn for _, rn, _ in w98)
print(f"  按 base reg: {dict(sorted(bases.items()))}")
for o, rn, rt in w98:
    print(f"    {o:#x}: str x{rt} -> [x{rn}, #0x98]")