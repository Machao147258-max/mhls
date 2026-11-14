# -*- coding: utf-8 -*-
"""修复 adrp 解码 (immhi<<14 | immlo<<12) 后重扫引用者:
1) 0xdebaa8 'certificate verify failed' -> ssl_verify_cert_chain
2) 0xdc61d0 'x509_vfy.c' -> X509_verify_cert 等
3) 0xdc6228 'x509_lu.c' -> get_by_subject 族"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def scan_refs(str_va, name, win=0x1000):
    page = str_va & ~0xFFF
    off = str_va - page
    found = []
    for lo, hi in [(0x0, 0x10022b8), (0x1574000, len(d)-8)]:
        for o in range(lo, hi-4, 4):
            w1 = struct.unpack_from('<I', d, o)[0]
            if (w1 & 0x9F000000) == 0x90000000:  # adrp (bits30-29=00 immlo; 宽掩码)
                rd = w1 & 0x1F
                # imm = PC_page + (immhi<<14 | immlo<<12)
                immhi = (w1 >> 5) & 0x7FFFF          # 19 位
                immlo = (w1 >> 29) & 0x3             # 2 位
                imm = (immhi << 14) | (immlo << 12)
                # 符号扩展 21 位
                if imm & 0x100000: imm -= 0x200000
                tgt_page = (o & ~0xFFF) + imm
                if tgt_page == page:
                    for j in range(o+4, min(o+win, hi-4), 4):
                        w2 = struct.unpack_from('<I', d, j)[0]
                        if (w2 & 0x1F) != rd: continue
                        if (w2 & 0xFFC00000) == 0x91000000:  # add imm
                            off2 = (w2 >> 10) & 0xFFF
                            if off2 == off:
                                found.append((o, j, 'add'))
                        elif (w2 & 0xFFC00000) == 0xF9400000:  # ldr
                            off2 = ((w2 >> 10) & 0xFFF) << 3
                            if off2 == off:
                                found.append((o, j, 'ldr'))
    print(f"[{name}] {str_va:#x} 页{page:#x} off{off:#x}: {len(found)} 引用")
    for a, b, t in found:
        print(f"    adrp@{a:#x} {t}@{b:#x}")
    return found

# 自检: 直接验证 0xbc4afc 的 adrp 解码
w = struct.unpack_from('<I', d, 0xbc4afc)[0]
immhi = (w >> 5) & 0x7FFFF
immlo = (w >> 29) & 3
imm = (immhi << 14) | (immlo << 12)
if imm & 0x100000: imm -= 0x200000
print(f"[自检] 0xbc4afc 指令 {w:#x} -> 目标页 {(0xbc4afc & ~0xFFF) + imm:#x} (期望 0xdc6000)")

scan_refs(0xdebaa8, "certificate verify failed")
scan_refs(0xdc61d0, "x509_vfy.c")
scan_refs(0xdc6228, "x509_lu.c")