# -*- coding: utf-8 -*-
"""1) 反汇编 0xbc8f60~0xbc90d0 (0xbc8e74 函数尾部)
2) 汇总 bl->0xbc84dc 及 bl->0xbc8b5c 全部调用者清单"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
REGIONS = [(0x0, 0x10022b8), (0x1574000, len(d) - 4)]

print("========== 1) 反汇编 0xbc8f60~0xbc90d0 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc8f60:0xbc90d0], 0xbc8f60):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n========== 2) bl -> 0xbc84dc 全部调用者 ==========")
hits = {}
for lo, hi in REGIONS:
    for o in range(lo, hi, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFC000000) == 0x94000000:
            delta = w & 0x03FFFFFF
            if delta >= 0x02000000: delta -= 0x04000000
            tgt = o + (delta << 2)
            if tgt == 0xbc84dc:
                hits.setdefault(hex(o), 0)
print(f"  bl->0xbc84dc 共 {len(hits)} 处: {sorted(hits)}")

print("\n========== 3) bl -> 0xbc8b5c 全部调用者 ==========")
hits2 = []
for lo, hi in REGIONS:
    for o in range(lo, hi, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFC000000) == 0x94000000:
            delta = w & 0x03FFFFFF
            if delta >= 0x02000000: delta -= 0x04000000
            tgt = o + (delta << 2)
            if tgt == 0xbc8b5c:
                hits2.append(o)
print(f"  {len(hits2)} 处: {[hex(h) for h in sorted(hits2)]}")

print("\n========== 4) bl -> 0xbc8aec (X509_OBJECT_free?) 全部调用者 ==========")
hits3 = []
for lo, hi in REGIONS:
    for o in range(lo, hi, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFC000000) == 0x94000000:
            delta = w & 0x03FFFFFF
            if delta >= 0x02000000: delta -= 0x04000000
            tgt = o + (delta << 2)
            if tgt == 0xbc8aec:
                hits3.append(o)
print(f"  {len(hits3)} 处: {[hex(h) for h in sorted(hits3)]}")