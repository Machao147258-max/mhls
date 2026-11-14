# -*- coding: utf-8 -*-
"""反汇编 str#0x98+0xa0 候选函数 + dump 0x17cd7b0/0x1873950 结构"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

print("=== A) dump 0x17cd7b0 ~ 0x17cd940 (结构A) ===")
for o in range(0x17cd7b0, 0x17cd940, 0x40):
    line = ' '.join(f'{struct.unpack_from("<Q", d, o+i*8)[0]:#x}' for i in range(8))
    print(f"  {o:#x}: {line}")

print("\n=== B) dump 0x1873950 ~ 0x18740e0 (结构B) ===")
for o in range(0x1873950, 0x18740e0, 0x40):
    line = ' '.join(f'{struct.unpack_from("<Q", d, o+i*8)[0]:#x}' for i in range(8))
    print(f"  {o:#x}: {line}")

print("\n=== C) 候选函数反汇编 ===")
for start, end, name in [(0x3c1300, 0x3c1400, 'cand@0x3c1368'),
                          (0x42a500, 0x42a5c0, 'cand@0x42a570'),
                          (0x56bf80, 0x56c000, 'cand@0x56bff4'),
                          (0x56c240, 0x56c300, 'cand@0x56c2bc'),
                          (0x584b60, 0x584c10, 'cand@0x584bc8'),
                          (0x3dab20, 0x3dac00, 'cand@0x3dab64')]:
    print(f"\n  --- {name} ({start:#x}~{end:#x}) ---")
    for ins in md.disasm(d[start:end], start):
        print(f"    {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")