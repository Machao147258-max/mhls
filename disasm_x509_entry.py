# -*- coding: utf-8 -*-
"""反汇编 0xbc8c00~0xbc9400 定位 X509_verify_cert 入口"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc8c00:0xbc9400], 0xbc8c00):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")