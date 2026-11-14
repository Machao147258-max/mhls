# -*- coding: utf-8 -*-
"""精确扫描 SSL_CTX_set_cert_verify_callback 注册点:
   str x1,[b,#0x98] 紧跟 str x2,[b,#0xa0] (或邻近 1-8 条指令)
   并 dump 0xdc6b48 / 0xdc6b58 附近字符串
"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

# 收集所有 str xRt,[xRn,#imm]  imm==0x98/0xa0
stores = []  # (addr, rn, rt, imm)
for o in range(0x0, 0x10022b8-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0xF9000000:
        imm = ((w >> 10) & 0xFFF) << 3
        if imm in (0x98, 0xa0):
            stores.append((o, (w>>5)&0x1F, w&0x1F, imm))

# 紧邻/近邻模式: base 相同, 0x98 在前 0xa0 在后, 距离 <= 0x20
print("=== A) str#0x98 → str#0xa0 同base 近邻 (注册点候选) ===")
found = []
for i,(a1,b1,t1,i1) in enumerate(stores):
    if i1 != 0x98: continue
    for a2,b2,t2,i2 in stores:
        if i2 != 0xa0 or b2 != b1: continue
        gap = a2 - a1
        if 0 < gap <= 0x20:
            found.append((a1,a2,b1,t1,t2,gap))
print(f"  近邻候选 {len(found)}:")
for f in found[:30]:
    print(f"    {f[0]:#x}->{f[1]:#x} base=x{f[2]} v=x{f[3]}/x{f[4]} gap={f[5]}")

print("\n=== B) 0xdc6b48 / 0xdc6b58 字符串 ===")
for addr in (0xdc6b40, 0xdc6b48, 0xdc6b58):
    s = d[addr:addr+64]
    end = s.find(b'\x00')
    print(f"  {addr:#x}: {s[:end]!r}")