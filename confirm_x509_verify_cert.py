# -*- coding: utf-8 -*-
"""1) 反汇编 0xbc8ca0~0xbc8e74 (X509_verify_cert 候选完整函数)
2) 字节级扫描 bl -> 0xbc8ca0 的调用者 (ssl_verify_cert_chain / ssl3_get_server_certificate)
3) 顺带扫描 bl -> 0xbc8e74 (下层函数)"""
from capstone import *
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("========== 1) 反汇编 0xbc8ca0~0xbc8e74 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc8ca0:0xbc8e74], 0xbc8ca0):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

def scan_bl(target, name):
    hits = []
    for o in range(0, 0x10022b8 - 4, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if w & 0xFC000000 == 0x94000000:
            delta = w & 0x03FFFFFF
            if delta >= 0x02000000: delta -= 0x04000000
            tgt = o + (delta << 2)
            if tgt == target:
                hits.append(o)
    for o in range(0x1574000, len(d) - 4, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if w & 0xFC000000 == 0x94000000:
            delta = w & 0x03FFFFFF
            if delta >= 0x02000000: delta -= 0x04000000
            tgt = o + (delta << 2)
            if tgt == target:
                hits.append(o)
    print(f"\nbl -> {name} ({target:#x}): {len(hits)} 处")
    for h in hits:
        print(f"  0x{h:#x}")
    return hits

print("\n========== 2) 调用者扫描 ==========")
scan_bl(0xbc8ca0, "X509_verify_cert")
scan_bl(0xbc8e74, "bc8e74")