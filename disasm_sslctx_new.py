# -*- coding: utf-8 -*-
"""1) 反汇编 0xc8b760~0xc8b900 (0xc8b838 疑似 SSL_CTX_new): 看 ctx+0x98/+0xa0 初始化
2) 反汇编 0xc91730~0xc91820: 确认 adrp/add 目标 (是否取 0xbc5e4c 地址)
3) 0xc8baf8 / 0xc8b9b0 快速识别"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

def dis(lo, hi, tag, maxins=300):
    print(f"\n=== {tag} ({lo:#x}~{hi:#x}) ===")
    for i, ins in enumerate(md.disasm(d[lo:hi], lo)):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        if i > maxins: 
            print("  ... trunc")
            break

dis(0xc8b760, 0xc8b900, '0xc8b838 (怀疑 SSL_CTX_new)')
dis(0xc91730, 0xc91820, '0xc917xx adrp/add 目标确认')
dis(0xc8baf8, 0xc8bb80, '0xc8baf8')
dis(0xc8b980, 0xc8ba30, '0xc8b9b0')