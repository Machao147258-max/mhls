# -*- coding: utf-8 -*-
"""反汇编 heartbeat 分支 0xc803ac (ssl3_read_bytes 内 TLS1_RT_HEARTBEAT 处理)"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True
lo, hi = 0xc80380, 0xc80600
for ins in md.disasm(d[lo:hi], lo):
    print(f"{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")