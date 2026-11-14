# -*- coding: utf-8 -*-
"""反汇编 5 个 X509_verify_cert 调用点上下文 (±0x30) 确认调用方身份"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

sites = [0xbc72f0, 0xbd9d34, 0xc80ff8, 0xc88ad4, 0xc8f05c]
for s in sites:
    print(f"\n===== 调用点 {s:#x} (0x{s-0x30:x}~0x{s+0x40:x}) =====")
    for ins in md.disasm(d[s-0x30:s+0x40], s-0x30):
        if ins.mnemonic in ('bl', 'blr', 'b', 'cbz', 'cbnz', 'tbz', 'tbnz') or ins.address >= s-0x8:
            print(f"  {ins.address:#08x}: {ins.mnemonic:8s} {ins.op_str}")