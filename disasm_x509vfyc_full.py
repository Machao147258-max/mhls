# -*- coding: utf-8 -*-
"""完整反汇编 0xbc4a00~0xbc4d00 与 0xbc5d40~0xbc6d00,
打印所有立即数 (mov/movz/add w4 等), 辅助识别 ERR 行号"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

for lo, hi, tag in [(0xbc4a00, 0xbc4d00, 'A'), (0xbc5d40, 0xbc6d00, 'B')]:
    print(f"\n========== region {tag} {lo:#x}~{hi:#x} ==========")
    for ins in md.disasm(d[lo:hi], lo):
        line = f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}"
        if '#' in ins.op_str and ('w4' in ins.op_str or 'x4' in ins.op_str):
            line += '   <<<< w4'
        print(line)