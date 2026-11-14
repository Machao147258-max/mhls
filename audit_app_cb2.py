# -*- coding: utf-8 -*-
"""1) 完整反汇编 ssl_verify_cert_chain 0xc8ef60~0xc8f070 理清 app_verify_callback 控制流
2) 扫描 'str X,[B,#0x98] + str Y,[B,#0xa0] 同基址相邻/相近' 的 app_verify_callback 注册点"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

print("=== 1) ssl_verify_cert_chain 完整 (0xc8ef60~0xc8f070) ===")
for ins in md.disasm(d[0xc8ef60:0xc8f070], 0xc8ef60):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== 2) str #0x98 + str #0xa0 同基址 (app_verify_callback 注册点候选) ===")
rows = []  # (addr, base_reg, val_reg, imm)
for o in range(0x0, 0x10022b8-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0xF9000000:  # str xRt, [xRn, #imm]
        imm = ((w >> 10) & 0xFFF) << 3
        if imm in (0x98, 0xa0):
            rn = (w >> 5) & 0x1F
            rt = w & 0x1F
            rows.append((o, rn, rt, imm))

# 找同 base 的 0x98 与 0xa0 对 (window ±0x40)
cands = []
for i, (a1, b1, t1, i1) in enumerate(rows):
    if i1 != 0x98: continue
    for a2, b2, t2, i2 in rows:
        if i2 != 0xa0 or b2 != b1: continue
        if 0 < a2 - a1 < 0x40 or 0 < a1 - a2 < 0x40:
            cands.append((min(a1, a2), max(a1, a2), b1, t1, t2))
print(f"  候选 {len(cands)} 组:")
for c in cands[:40]:
    print(f"    {c[0]:#x}~{c[1]:#x} base=x{c[2]} val=x{c[3]}/x{c[4]}")