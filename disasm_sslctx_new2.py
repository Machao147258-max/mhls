# -*- coding: utf-8 -*-
"""1) 反汇编 0xc8c300~0xc8c5c0 (SSL_CTX_new=0xc8c464) 确认 ctx+0x98 默认值
2) 重放 0xc8b760~0xc8b900 (0xc8b7f8 写+0x98 分支的确切行为)
3) 读字符串 0x8da944 / 0x8dacfc / 0x8d9xxx"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

def dis(lo, hi, tag, maxins=500):
    print(f"\n=== {tag} ({lo:#x}~{hi:#x}) ===")
    for i, ins in enumerate(md.disasm(d[lo:hi], lo)):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        if i > maxins:
            print("  ... trunc")
            break

def show_str(addr, n=96):
    raw = d[addr:addr+n]
    s = raw.split(b'\x00')[0]
    try:
        print(f"  str@{addr:#x}: {s.decode('utf-8', 'replace')!r}")
    except Exception:
        print(f"  str@{addr:#x}: {s!r}")

dis(0xc8c300, 0xc8c5c0, '0xc8c464 SSL_CTX_new')
dis(0xc8b760, 0xc8b900, '0xc8b7f8 完整')
print("\n=== 字符串 ===")
for a in (0x8da944, 0x8dacfc, 0xd710f8, 0xd710128, 0xd710380, 0xd7101e8):
    show_str(a)