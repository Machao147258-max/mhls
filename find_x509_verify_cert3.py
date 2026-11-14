# -*- coding: utf-8 -*-
"""1) 字节级扫描 bl -> 0xbc93a8 (get_by_subject) 的调用者 => X509_verify_cert
   2) 反汇编 0xbc8000~0xbc8ca0"""
from capstone import *
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

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
    print(f"bl -> {name} ({target:#x}): {len(hits)} 处")
    for h in hits:
        print(f"  0x{h:#x}")
    return hits

print("=========== 调用者扫描 ===========")
c1 = scan_bl(0xbc93a8, "X509_STORE_CTX_get_by_subject")
c2 = scan_bl(0xbc9df8, "X509_verify_cert_error_string")
c3 = scan_bl(0xbc8b5c, "0xbc8b5c(idx?)")
c4 = scan_bl(0xbc8b14, "0xbc8b14")

print("\n=========== 反汇编 0xbc8000~0xbc8ca0 ===========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc8000:0xbc8ca0], 0xbc8000):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")