# -*- coding: utf-8 -*-
"""1) 反汇编 0xb9828c / 0xb981f8 (被0x3c1368写入 +0x98/+0xa0 的来源)
2) 反汇编 0x3c1300 函数开头 (找起点特征) 及引用全局对象 0x1586838 的代码
3) 验证 0x1586838 是否是 SSL_CTX/默认配置: 全库搜索引用它的 adrp"""
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

dis(0xb98280, 0xb98300, '0xb9828c')
dis(0xb981e0, 0xb98260, '0xb981f8')

print("\n=== 2) 0x3c1300 函数起点回溯 ===")
# 向上找函数开头: 找 0x3c1300 之前最近的 stp x29,x30 / sub sp
for o in range(0x3c1300-0x200, 0x3c1300, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFFFFC1F) == 0xA9800000 or (w & 0xFF800000) == 0xD1000000:  # stp x29,x30,[sp,#imm]! 或 sub sp,sp,#imm
        print(f"  函数起点候选 {o:#x}: {w:#x}")
        dis(o, 0x3c1300, f'func start @ {o:#x}')
        break

print("\n=== 3) 全局对象 0x1586838 引用 (adrp 0x1586000) ===")
hits = []
for o in range(0x0, 0x10022b8-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    # adrp x?, 0x1586000 : immhi/immlo 编码, page 0x1586000
    if (w & 0x9F000000) == 0x90000000:
        immhi = (w >> 5) & 0x7FFFF
        immlo = (w >> 29) & 0x3
        imm = (immhi << 14) | (immlo << 12)
        if imm & 0x100000: imm -= 0x200000
        page = ((o >> 12) << 12) + imm
        if page == 0x1586000:
            hits.append(o)
print(f"  adrp->0x1586000: {len(hits)} 处")
for h in hits[:20]:
    print(f"    {h:#x}")