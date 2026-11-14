# -*- coding: utf-8 -*-
"""核查: 1) dtls1_read_bytes 是否另有 0x18 心跳分支; 2) 0xb99964 头部确认 OPENSSL_malloc"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True

print("=== 1) 0xb99964 头部 (疑似 OPENSSL_malloc 3参) ===")
for ins in md.disasm(d[0xb99964:0xb99a20], 0xb99964):
    print(f"  {ins.address:#x}: {ins.mnemonic:7s} {ins.op_str}")

print("\n=== 2) 所有 cmp #0x18 候选周边的 bl 目标 (找 dtls 心跳分发) ===")
import re
cands = []
for lo in range(0, 0x10022b8, 0x8000):
    hi = min(lo + 0x8000, 0x10022b8)
    seq = list(md.disasm(d[lo:hi], lo))
    for i, ins in enumerate(seq):
        if ins.mnemonic == 'cmp' and ins.op_str.endswith('#0x18'):
            # 收集接下来 0x30 内的 bl
            bls = []
            for j in range(i+1, min(i+12, len(seq))):
                if seq[j].mnemonic == 'bl':
                    bls.append(int(seq[j].op_str[1:], 16))
            cands.append((ins.address, bls[:3]))
for a, bls in cands:
    tag = ''
    if any(0xc80000 <= b <= 0xc90000 for b in bls): tag = ' <== SSL区'
    print(f"  0x{a:#x}: bl {[hex(b) for b in bls]}{tag}")