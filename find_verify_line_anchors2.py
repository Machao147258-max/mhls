# -*- coding: utf-8 -*-
"""修正版: MOVZ W4,#imm16 (0x52800000) + bl 26位符号扩展, 提取 0xbc4a00~0xbc6d00 各 ERR 调用点行号"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
lo, hi = 0xbc4a00, 0xbc6d00

adds = []
for o in range(lo, hi-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0x91000000 and ((w >> 10) & 0xFFF) == 0x1d0:
        rd, rn = w & 0x1F, (w >> 5) & 0x1F
        if rd == rn:
            adds.append(o)
print(f"add #0x1d0: {len(adds)} 处")

def find_movw4(a):
    for o in range(max(lo, a-0x50), a+0x4, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFFFFFC00) == 0x52800000:  # MOVZ Wd
            rd = w & 0x1F
            if rd == 4:
                return o, (w >> 5) & 0xFFFF
    return None, None

def find_bl_after(a):
    for j in range(a+4, min(a+0x40, hi-4), 4):
        w = struct.unpack_from('<I', d, j)[0]
        if (w & 0xFC000000) == 0x94000000:
            imm26 = w & 0x3FFFFFF
            if imm26 & 0x2000000: imm26 -= 0x4000000
            tgt = j + (imm26 << 2)
            return j, tgt
    return None, None

for a in adds:
    mo, line = find_movw4(a)
    bj, bt = find_bl_after(a)
    ln = line if line is not None else -1
    role = ''
    if ln > 0:
        if 0x280 <= ln <= 0x3a0: role = '  <<< X509_verify_cert ERRange 候选'
        elif ln == 0x5d0: role = '  (=1488 X509_STORE_CTX_verify_cert)'
        elif ln >= 0x4b0: role = '  (0x4xx 高段)'
        elif ln < 0x280: role = '  (低段)'
    print(f"add@{a:#x} line={ln:#x}({ln}){role}  bl@{bj:#x}->{bt:#x}" if mo else f"add@{a:#x} line=-- bl@{bj:#x}->{bt:#x}")