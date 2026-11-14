# -*- coding: utf-8 -*-
"""libepay-crypto.so: 反汇编 0x44f00-0x45380 JNI 注册函数, 提取 fnPtr"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True
lo, hi = 0x44e80, 0x453c0
for ins in md.disasm(d[lo:hi], lo):
    print(f"{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")