# -*- coding: utf-8 -*-
"""决定性确认: 0xc91700~0xc91830 的 adrp+add 目标 + 0xc8c84c 上下文"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

def dis(lo, hi, tag):
    print(f"\n=== {tag} ({lo:#x}~{hi:#x}) ===")
    for ins in md.disasm(d[lo:hi], lo):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

# 1) 0xc9174c 附近: 一个 adrp+add 序列 (可能是函数入口的常量装载)
dis(0xc91730, 0xc91830, '0xc917xx adrp/add 序列')

# 2) 0xc8c84c str [x0,#0x98]
dis(0xc8c800, 0xc8c900, '@0xc8c84c str [x0,#0x98]')

# 3) 0xc92da8/x6, 0xc92df8 等 (另一群)
dis(0xc92d80, 0xc92e80, '0xc92dxx adrp/add 序列')

# 4) 0xc9cce4 / 0xc9cd38
dis(0xc9ccb0, 0xc9cd90, '0xc9ccxx adrp/add 序列')