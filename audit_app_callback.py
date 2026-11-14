# -*- coding: utf-8 -*-
"""1) 反汇编 0xc8f040~0xc8f068 (verify_mode 分支)
2) 扫描所有 str x?, [x?, #0x98] 指令 -> app_verify_callback 注册点候选
3) 重新扫描 bl -> 0xbc4a1c / 0xbc5e4c 全部调用者 (含数据段指针表调用确认)
4) 检查 0x17cd7f0 / 0x1873990 指针表周边"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

print("=== 1) 0xc8f040~0xc8f068 ===")
for ins in md.disasm(d[0xc8f040:0xc8f068], 0xc8f040):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== 2) str x?, [x?, #0x98] 指令 (写入字段+0x98) ===")
found = []
for o in range(0x0, 0x10022b8-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    # str x reg, [xreg, #0x98] : 1111100100 imm12 Rn Rt ; 0xF9000000 | (0x98>>3)<<10 | Rn<<5 | Rt
    if (w & 0xFFC00000) == 0xF9000000 and ((w >> 10) & 0xFFF) == 0x13:  # 0x98>>3 = 0x13
        found.append(o)
print(f"  {len(found)} 处: {[hex(x) for x in found[:30]]}")

print("\n=== 3) bl -> 0xbc4a1c (X509_STORE_CTX_verify_cert) ===")
callers_4a1c = []
callers_5e4c = []
for lo, hi in [(0x0, 0x10022b8-4), (0x1574000, len(d)-4)]:
    for o in range(lo, hi-4, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFC000000) == 0x94000000:
            imm26 = w & 0x3FFFFFF
            if imm26 & 0x2000000: imm26 -= 0x4000000
            t = o + (imm26 << 2)
            if t == 0xbc4a1c: callers_4a1c.append(o)
            if t == 0xbc5e4c: callers_5e4c.append(o)
print(f"  bl->0xbc4a1c: {len(callers_4a1c)} 处 {[hex(x) for x in callers_4a1c]}")
print(f"  bl->0xbc5e4c: {len(callers_5e4c)} 处 {[hex(x) for x in callers_5e4c]}")

print("\n=== 4) 0x17cd7f0 / 0x1873990 指针表周边 (前后各 8 项) ===")
for base in (0x17cd7f0, 0x1873990):
    print(f"  --- 表 {base:#x} ---")
    for k in range(-8, 9):
        a = base + k*8
        v = struct.unpack_from('<Q', d, a)[0]
        print(f"    [{a:#x}] = {v:#x}  ({'代码区' if v < 0x10022b8 else '数据区'})")