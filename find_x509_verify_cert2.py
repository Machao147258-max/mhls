# -*- coding: utf-8 -*-
"""1) 反汇编 0xbc9400~0xbc9800 (X509_verify_cert 入口候选)
2) 字节级扫描 bl/target=0xbc9df8 的编码 验证有无直接调用
3) 向前扫描更多函数序言定位 X509_verify_cert"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("======== 1) 反汇编 0xbc9400~0xbc9df8 ========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc9400:0xbc9800], 0xbc9400):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n======== 2) 字节级 bl->0xbc9df8 编码匹配 ========")
import struct
TGT = 0xbc9df8
def bl_imm(ins_addr, target):
    delta = (target - ins_addr) >> 2
    return 0x94000000 | (delta & 0x03FFFFFF)
hits = []
for o in range(0, 0x10022b8 - 4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if w & 0xFC000000 == 0x94000000:
        delta = w & 0x03FFFFFF
        if delta >= 0x02000000: delta -= 0x04000000
        tgt = o + (delta << 2)
        if tgt == TGT:
            hits.append(o)
for o in range(0x1574000, len(d) - 4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if w & 0xFC000000 == 0x94000000:
        delta = w & 0x03FFFFFF
        if delta >= 0x02000000: delta -= 0x04000000
        tgt = o + (delta << 2)
        if tgt == TGT:
            hits.append(o)
print(f"bl->0xbc9df8 命中 {len(hits)} 处 (vaddr)")
for h in hits: print(f"  0x{h:#x}")

print("\n======== 3) 0xbc8c00~0xbc9400 扫描函数序言 ========")
# 找 stp x29,x30,[sp,#-N]! 模式: FD 7B  B? A9  (0xA9B87BFD 等)
pro = []
for o in range(0xbc8c00, 0xbc9800 - 4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    # stp x29,x30,[sp,#-imm]! 编码: 0xA9800000 | (imm<<10)... 简化: opcode 高字节 A9 B? 
    if (w & 0xFFC00000) == 0xA9800000 and ((w >> 5) & 0x1F) == 29 and ((w >> 0) & 0x1F) == 30:
        imm = ((w >> 22) & 0x1F) | ((w >> 15) & 0x7F)  # 简化
        pro.append((o, w))
for o, w in pro:
    print(f"  序言 @ {o:#x}  w={w:#010x}")