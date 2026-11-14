# -*- coding: utf-8 -*-
"""紧凑输出: 心跳特征分段查询(总输出<2KB)
A1: cmp w?,#0x18 地址 + 周边 bl"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True
CODE_END = 0x10022b8
out = []
for lo in range(0, CODE_END, 0x8000):
    hi = min(lo + 0x8000, CODE_END)
    for ins in md.disasm(d[lo:hi], lo):
        if ins.mnemonic == 'cmp' and ins.op_str.endswith('#0x18'):
            out.append(ins.address)
print("N_cmp18=%d" % len(out))
print(",".join(hex(a) for a in out))