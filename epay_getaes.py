# -*- coding: utf-8 -*-
"""libepay-crypto.so: 1) 反汇编 0x44f30-0x45030 看 x20/密钥缓冲构造  2) getAesKey 0x4a6fc 全函数"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True

print("=== 0x44f30 - 0x45030 (XOR 解密例程) ===")
for ins in md.disasm(d[0x44f30:0x45030], 0x44f30):
    print(f"{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== getAesKey @ 0x4a6fc (全函数) ===")
for ins in md.disasm(d[0x4a6fc:0x4a6fc+0x200], 0x4a6fc):
    print(f"{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")