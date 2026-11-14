# -*- coding: utf-8 -*-
"""1) 扫描 bl -> 0xc8c84c (SSL_CTX_set_cert_verify_callback) 的调用者
2) 扫描数据段 qword 指向 0xc8c84c / 0xc8c844 的引用
3) 若找到调用者, 反汇编其上下文"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
CODE_END = 0x10022b8

TARGET = {0xc8c84c: 'SSL_CTX_set_cert_verify_callback',
          0xc8c844: 'SSL_CTX_set_verify',
          0xc8c83c: 'setter@0xa8',
          0xc8c858: 'setter@0x150/0x178'}

print("=== 1) bl -> setter 调用者 ===")
bl_hits = {}
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFC000000) == 0x94000000:
        imm26 = w & 0x3FFFFFF
        if imm26 & 0x2000000: imm26 -= 0x4000000
        t = o + (imm26 << 2)
        if t in TARGET:
            bl_hits.setdefault(t, []).append(o)
for t, addrs in bl_hits.items():
    print(f"  bl->{TARGET[t]} ({t:#x}): {len(addrs)} 处")
    for a in addrs:
        print(f"    {a:#x}")
        # 反汇编调用前后
        lo, hi = a-0x20, min(a+0x10, CODE_END)
        for ins in md.disasm(d[lo:hi], lo):
            print(f"      {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== 2) 数据段 qword 引用 ===")
refs = {}
for o in range(0x10022b8, len(d)-8, 8):
    v = struct.unpack_from('<Q', d, o)[0]
    if v in TARGET:
        refs.setdefault(v, []).append(o)
for v, addrs in refs.items():
    print(f"  {TARGET[v]} ({v:#x}): {len(addrs)} 处 -> {[hex(x) for x in addrs[:10]]}")

print("\n=== 3) 也扫 adrp+add 取地址 (代码区引用 0xc8c84c) ===")
# adrp 到 0xc8c000 页
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0x9F000000) == 0x90000000:
        immhi = (w >> 5) & 0x7FFFF
        immlo = (w >> 29) & 0x3
        imm = (immhi << 14) | (immlo << 12)
        if imm & 0x100000: imm -= 0x200000
        page = ((o >> 12) << 12) + imm
        if page == 0xc8c000:
            rd = w & 0x1F
            nxt = struct.unpack_from('<I', d, o+4)[0]
            dest = None
            if (nxt & 0xFFC00000) == 0x91000000 and ((nxt>>5)&0x1F) == rd:
                dest = 0xc8c000 + ((nxt >> 10) & 0xFFF)
            if dest in (0xc8c84c, 0xc8c844, 0xc8c83c):
                print(f"  {o:#x}: adrp+add -> {dest:#x} ({TARGET.get(dest,'?')})")