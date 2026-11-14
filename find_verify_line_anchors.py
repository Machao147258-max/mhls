# -*- coding: utf-8 -*-
"""提取 0xbc4a00~0xbc6d00 区所有 ERR_put_error 调用点的行号/常量/文件串偏移，
按行号聚类定位 X509_verify_cert (行~640-900)"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True

lo, hi = 0xbc4a00, 0xbc6d00
# 先找所有 add Xn,Xn,#0x1d0 (DC61D0 页内偏移)
adds = []
for o in range(lo, hi-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0x91000000 and ((w >> 10) & 0xFFF) == 0x1d0:
        rd = w & 0x1F
        rn = (w >> 5) & 0x1F
        if rd == rn:
            adds.append(o)
print(f"add #0x1d0 (同 rd/rn) 命中 {len(adds)} 处: {[hex(a) for a in adds]}\n")

# 对每处 add，在 ±0x30 内找 mov w4,#line 与紧随的 bl 错误处理
ERR_BLS = {0xbac7c8, 0xb98ec0, 0xc26038}
lines = []
for a in adds:
    best = None
    for o in range(max(lo, a-0x40), a+0x10, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFFFFFC00) == 0x72800000:  # mov w4, #imm16 (四舍五入 0x72800000|(imm<<5)|4)
            imm = (w >> 5) & 0xFFFF
            if 0 < imm < 0x800:
                best = (o, imm)
    # 找紧随的 bl
    bl_t = None
    for j in range(a+4, min(a+0x30, hi-4), 4):
        w = struct.unpack_from('<I', d, j)[0]
        if (w & 0xFC000000) == 0x94000000:
            tgt = j + ((w & 0x3FFFFFF) << 2)
            if tgt > 0x100000000: tgt -= 0x100000000
            bl_t = (j, tgt)
            break
    lines.append((a, best, bl_t))

for a, best, bl_t in lines:
    ln = best[1] if best else -1
    # 由行号推测身份
    role = ''
    if ln >= 0:
        if 0x280 <= ln <= 0x390 and ln != 0x2dc: role = '<- X509_verify_cert 候选'
        elif ln == 0x5d0: role = 'X509_STORE_CTX_verify_cert(已知)'
        elif ln >= 0x500: role = 'check_revocation/等 0x5xx'
        elif ln < 0x280: role = '低行号(早段函数)'
    print(f"add@{a:#x}  movw4(line)@{best[0]:#x}=0x{ln:x}({ln})  bl@{bl_t}" if best else f"add@{a:#x}  no-line  bl@{bl_t}")