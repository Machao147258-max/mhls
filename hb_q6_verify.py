# -*- coding: utf-8 -*-
"""验证: 1) 0x3b5920=memcpy? 2) 0xc7f150=ssl3_write_bytes(参数形态) 3) DTLS 心跳分支副本"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True

print("=== 1) 0x3b5920 函数头部 (疑似 memcpy) ===")
for ins in md.disasm(d[0x3b5920:0x3b59c0], 0x3b5920):
    print(f"  {ins.address:#x}: {ins.mnemonic:7s} {ins.op_str}")

print("\n=== 2) 0xc7f150 函数头 (疑似 ssl3_write_bytes, 参数 s/type/buf/len) ===")
for ins in md.disasm(d[0xc7f150:0xc7f220], 0xc7f150):
    print(f"  {ins.address:#x}: {ins.mnemonic:7s} {ins.op_str}")

print("\n=== 3) DTLS/其他 heartbeat REQUEST 副本扫描: bl 0xb99964 且前有 add #0x13 且后接 strb #2/0x18 ===")
cands = []
for lo in range(0, 0x10022b8, 0x8000):
    hi = min(lo + 0x8000, 0x10022b8)
    seq = list(md.disasm(d[lo:hi], lo))
    for i, ins in enumerate(seq):
        if ins.mnemonic == 'bl' and ins.op_str == '#0xb99964':
            ctx = seq[max(0,i-4):i]
            pre = '; '.join(f"{s.mnemonic} {s.op_str}" for s in ctx)
            if '#0x13' in pre:
                cands.append((ins.address, pre))
print(f"  共 {len(cands)} 处 malloc 前 add#0x13; 列表前 10:")
for a, pre in cands[:10]:
    print(f"    0x{a:#x}  pre: {pre[:120]}")