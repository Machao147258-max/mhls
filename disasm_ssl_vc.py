# -*- coding: utf-8 -*-
"""完整反汇编 ssl_verify_cert_chain 候选 (0xc8ef60~0xc8f068) + X509层调用者上下文"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

for lo, hi, tag in [(0xc8ef60, 0xc8f068, 'ssl_verify_cert_chain?'), (0xbc7200, 0xbc73a0, 'x509 wrapper A'), (0xbd9cf0, 0xbd9de0, 'x509 wrapper B')]:
    print(f"\n===== {tag} {lo:#x}~{hi:#x} =====")
    for ins in md.disasm(d[lo:hi], lo):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
    print()