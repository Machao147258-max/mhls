# -*- coding: utf-8 -*-
"""反汇编多处候选点周边, 找 ssl3_read_bytes 心跳分支形态"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True
pts = [0xc830ec, 0xc7e690, 0xc7f9ac, 0xc251f4, 0xc256f4, 0xc25744]
for p in pts:
    lo = p - 0x30; hi = p + 0x90
    print(f"\n===== 0x{p:x} 周边 =====")
    for ins in md.disasm(d[lo:hi], lo):
        m = ins.mnemonic
        if m in ('ldrb','ldrh','ldr','cmp','b.eq','b.ne','b.ls','b.hi','tbnz','tbz','cbz','cbnz','bl','str','strb','mov','and','orr','lsl'):
            print(f"  {ins.address:#x}: {m:7s} {ins.op_str}")