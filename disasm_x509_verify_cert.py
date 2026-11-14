# -*- coding: utf-8 -*-
"""反汇编 0xbc93a8~0xbc9c00 (X509_verify_cert 候选完整函数体)"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc93a8:0xbc9c00], 0xbc93a8):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")