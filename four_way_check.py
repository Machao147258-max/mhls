# -*- coding: utf-8 -*-
"""四路并行验证:
1) 扫描 b (0x14000000) 与 b.cond (0x54000000/0x2A000000/0x2B000000) 尾调用目标 = 0xbc8ca0/0xbc8e74
2) 读 0x10908b0 全局指针
3) 反汇编 0xbc8e74~0xbc8f60
4) 宽窗口: adrp xN,#0xdc6000 后 ±0x80 内 同xN add #0x1d0 (x509_vfy.c 0xdc61d0)
"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
REGIONS = [(0x0, 0x10022b8), (0x1574000, len(d) - 4)]

print("========== 1) b / b.cond 尾调用扫描 ==========")
for target, name in [(0xbc8ca0, "bc8ca0"), (0xbc8e74, "bc8e74"), (0xbc8b5c, "bc8b5c"), (0xbc9df8, "error_string")]:
    hits = []
    for lo, hi in REGIONS:
        for o in range(lo, hi, 4):
            w = struct.unpack_from('<I', d, o)[0]
            # b 无条件
            if (w & 0xFC000000) == 0x14000000:
                delta = w & 0x03FFFFFF
                if delta >= 0x02000000: delta -= 0x04000000
                if o + (delta << 2) == target: hits.append((o, 'b'))
            # b.cond
            if (w & 0xFF000010) == 0x54000000:
                delta = (w >> 5) & 0x7FFFF
                if delta >= 0x40000: delta -= 0x80000
                if o + (delta << 2) == target: hits.append((o, 'b.cond'))
            # cbz/cbnz/tbz/tbnz 不太可能做尾调，跳过
    print(f"  -> {name} {target:#x}: {len(hits)} 处")
    for h, typ in hits[:20]:
        print(f"     0x{h:#x} ({typ})")

print("\n========== 2) 0x10908b0 指针区 ==========")
for off in range(0x1090800, 0x1090900, 8):
    v = struct.unpack_from('<Q', d, off)[0]
    if v > 0x1000:
        print(f"  {off:#x}: {v:#x}")

print("\n========== 3) 反汇编 0xbc8e74~0xbc8f60 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc8e74:0xbc8f60], 0xbc8e74):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n========== 4) x509_vfy.c (0xdc61d0) 引用者宽窗口 ==========")
page = 0xdc6000
hits = []
for lo, hi in REGIONS:
    for o in range(lo, hi - 8, 4):
        w1 = struct.unpack_from('<I', d, o)[0]
        if (w1 & 0x9F000000) == 0x90000000:
            rd1 = w1 & 0x1F
            imm1 = ((w1 >> 5) & 0x7FFFF) << 12
            if ((o & ~0xFFF) + imm1) == page:
                # ±0x100 窗口内找 add rd1,#0x1d0 或 add rd1,#0x1d0 变体
                for j in range(o + 4, min(o + 0x100, hi - 4), 4):
                    w2 = struct.unpack_from('<I', d, j)[0]
                    if (w2 & 0xFFC00000) == 0x91000000 and (w2 & 0x1F) == rd1:
                        off2 = (w2 >> 10) & 0xFFF
                        if (page + off2) == 0xdc61d0:
                            hits.append((o, j, 'add'))
                    if (w2 & 0xFFC00000) == 0xF9400000 and (w2 & 0x1F) == rd1:
                        off2 = ((w2 >> 10) & 0xFFF) << 3
                        if (page + off2) == 0xdc61d0:
                            hits.append((o, j, 'ldr'))
print(f"  命中 {len(hits)} 处:")
for a, b, t in hits:
    print(f"    adrp@0x{a:#x} -> {t}@0x{b:#x}")