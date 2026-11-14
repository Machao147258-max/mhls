# -*- coding: utf-8 -*-
"""专项: SSL_CTX_set_cert_verify_callback 注册点
A) 全代码区 str xRt,[xRn,#0x98], Rn=x0 (参数/this) — 原型候选, 附上下文
B) 全代码区 str #0x98 且 Rn 非 sp/x31/xzr 的全部候选 (含第2值 #0xa0)
C) 代码区对 0xbc5e4c 的 adrp+add 取地址引用 (SSL_CTX_new 默认初始化线索)"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
CODE_END = 0x10022b8

print("=== A) str [x0,#0x98] 全候选 ===")
a_hits = []
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0xF9000000:
        imm = ((w >> 10) & 0xFFF) << 3
        rn = (w >> 5) & 0x1F
        if imm == 0x98 and rn == 0:
            a_hits.append(o)
print(f"  str [x0,#0x98]: {len(a_hits)} 处 -> {[hex(x) for x in a_hits]}")
for h in a_hits[:16]:
    lo, hi = h-0x20, h+0x20
    print(f"\n  --- @{h:#x} 上下文 ---")
    for ins in md.disasm(d[lo:hi], lo):
        print(f"    {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== B) str [xRn,#0x98] Rn in {19,20,21,22,23,24,25} (非sp/非x0) ===")
b_hits = []
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0xF9000000:
        imm = ((w >> 10) & 0xFFF) << 3
        rn = (w >> 5) & 0x1F
        rt = w & 0x1F
        if imm == 0x98 and rn in range(19, 26):
            b_hits.append((o, rn, rt))
print(f"  {len(b_hits)} 处")
for h in b_hits:
    print(f"    {h[0]:#x}: str x{h[2]} -> [x{h[1]}, #0x98]")

print("\n=== C) 代码区对 0xbc5e4c 的取地址引用 (adrp 0xbc4000 + add #0x1e4c) ===")
c_hits = []
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0x9F000000) == 0x90000000:  # adrp
        immhi = (w >> 5) & 0x7FFFF
        immlo = (w >> 29) & 0x3
        imm = (immhi << 14) | (immlo << 12)
        if imm & 0x100000: imm -= 0x200000
        page = ((o >> 12) << 12) + imm
        if page == 0xbc4000:
            c_hits.append(o)
print(f"  adrp->0xbc4000: {len(c_hits)} 处")
for h in c_hits:
    # 看后续 add 是否 +0x1e4c
    w2 = struct.unpack_from('<I', d, h+4)[0] if h+4 < CODE_END else 0
    if (w2 & 0xFFC00000) == 0x91000000:  # add imm12
        imm12 = ((w2 >> 10) & 0xFFF)
        if ((w2 >> 5) & 0x1F) == ((w & 0x1F)):  # 同寄存器
            print(f"    {h:#x}: adrp + add #{imm12:#x} -> 目标 {0xbc4000+imm12:#x}")
        else:
            print(f"    {h:#x}: adrp (add rd=x{(w2>>5)&0x1F} 不同reg)")
    else:
        print(f"    {h:#x}: adrp (后续非add)")