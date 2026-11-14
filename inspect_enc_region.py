# -*- coding: utf-8 -*-
"""1) 反汇编 0xc874b0 / 0xc875a4 (判断函数身份)
2) 查看 0x3ad708 实例周围原始 qword (判断真实结构)"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

print("=== 实例区原始数据 0x3ad6c0-0x3ad820 ===")
import struct
o0 = 0x3ad6c0
for off in range(o0, o0+0x160, 8):
    q = struct.unpack_from('<Q', d, off)[0]
    note = ''
    if 0 <= q < 0x10022b8 or (0x15b1000 <= q < 0x1906000):
        note = ' [EXEC]'
    elif 0x1012e08 <= q < 0x1580540:
        note = ' [DATA]'
    elif q < 0x10000:
        note = ' [small]'
    if 0x10022b8 > q > 0x900000:
        try:
            s = d[q:q+32].split(b'\x00')[0]
            if all(32 <= c < 127 for c in s):
                note += f" -> '{s.decode()}'"
        except Exception:
            pass
    print(f"  {off:#x}: {q:#018x}{note}")

print("\n=== 反汇编 0xc87490-0xc87630 ===")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
code = d[v2off(0xc87490):v2off(0xc87630)]
for ins in md.disasm(code, 0xc87490):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")