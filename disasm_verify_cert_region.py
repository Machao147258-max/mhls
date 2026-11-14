# -*- coding: utf-8 -*-
"""反汇编 0xbc4100~0xbc4a1c (X509_verify_cert 候选区: x509_vfy.c 行150-470)"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc4100:0xbc4a1c], 0xbc4100):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")