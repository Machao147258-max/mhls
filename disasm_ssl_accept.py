# -*- coding: utf-8 -*-
"""从 SSL_accept@0xc8d6cc 向前后反汇编, 识别 1.0.1c ssl_lib.c wrapper 序列布局"""
from capstone import *
from capstone.arm64 import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

LOAD0_LO, LOAD0_HI = 0x0, 0x10022b8  # offset==vaddr

def voff(v):
    if LOAD0_LO <= v < LOAD0_HI:
        return v
    if 0x1012e08 <= v < 0x1580540:
        return v - 0x10000
    if 0x15b1000 <= v < 0x1906000:
        return v - 0x3d000
    return None

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

def disasm_range(start_v, nbytes, label=''):
    off = voff(start_v)
    code = d[off:off+nbytes]
    out = []
    for ins in md.disasm(code, start_v):
        out.append(f"  {hex(ins.address):>12}: {ins.mnemonic:8s} {ins.op_str}")
    print(f"--- {label} @ {hex(start_v)} ({nbytes}B) ---")
    print('\n'.join(out))

# SSL_accept @ 0xc8d6cc, 84B -> 再往前看 0xC8 (前导对齐)
disasm_range(0xc8d6cc - 0x40, 0x40, 'BEFORE SSL_accept')
disasm_range(0xc8d6cc, 0x200, 'SSL_accept @0xc8d6cc + next 0x200')