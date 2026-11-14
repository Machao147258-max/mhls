# -*- coding: utf-8 -*-
"""扫描 bl -> 各 x509_vfy.c 候选函数 的调用者:
0xbc4a1c / 0xbc49ac / 0xbc4b40 / 0xbc4bf8 / 0xbc4470 / 0xbc421c
同时反汇编 0xbc4b40~0xbc4c80 (x509_vfy.c 下一函数)"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
REGIONS = [(0x0, 0x10022b8), (0x1574000, len(d) - 4)]

print("========== 1) 调用者扫描 ==========")
for target, name in [(0xbc4a1c, "vfy.py? (X509_STORE_CTX_verify_cert?)"),
                     (0xbc49ac, "vfy.py? (set_error/current_cert)"),
                     (0xbc4b40, "vfy.py?"),
                     (0xbc4bf8, "vfy.py?"),
                     (0xbc4470, "x509 字符串处理"),
                     (0xbc421c, "x509 处理")]:
    hits = []
    for lo, hi in REGIONS:
        for o in range(lo, hi, 4):
            w = struct.unpack_from('<I', d, o)[0]
            if (w & 0xFC000000) == 0x94000000:
                delta = w & 0x03FFFFFF
                if delta >= 0x02000000: delta -= 0x04000000
                if o + (delta << 2) == target:
                    hits.append(o)
    print(f"  bl->{target:#x} ({name}): {len(hits)} 处 {[hex(h) for h in hits]}")

print("\n========== 2) 反汇编 0xbc4b40~0xbc4c80 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc4b40:0xbc4c80], 0xbc4b40):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")