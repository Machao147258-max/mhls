# -*- coding: utf-8 -*-
"""输出 bl->0xbc9df8 的 3 个调用点上下文 + 完整函数区间反汇编"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

import struct
TGT = 0xbc9df8
hits = []
for o in range(0, 0x10022b8 - 4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if w & 0xFC000000 == 0x94000000:
        delta = w & 0x03FFFFFF
        if delta >= 0x02000000: delta -= 0x04000000
        tgt = o + (delta << 2)
        if tgt == TGT:
            hits.append(o)
for o in range(0x1574000, len(d) - 4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if w & 0xFC000000 == 0x94000000:
        delta = w & 0x03FFFFFF
        if delta >= 0x02000000: delta -= 0x04000000
        tgt = o + (delta << 2)
        if tgt == TGT:
            hits.append(o)

print(f"bl->0xbc9df8 调用点: {[hex(h) for h in hits]}\n")

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

for h in hits:
    print(f"=========== 调用点 {h:#x} 上下文 (±0x100) ===========")
    for ins in md.disasm(d[max(0,h-0x100):h+0x120], max(0,h-0x100)):
        mark = '  <<<< 调用点' if ins.address == h else ''
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}{mark}")