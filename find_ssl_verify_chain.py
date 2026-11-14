# -*- coding: utf-8 -*-
"""定位 ssl_verify_cert_chain:
扫 "certificate verify failed"@0xdebaa8 页引用 (adrp #0xdeb000 + add #0xaa8, 宽窗口 ±0x800)
+ 加宽 x509_vfy.c (0xdc61d0) 引用 (adrp #0xdc6000 + add #0x1d0 宽窗口 ±0x800)"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def scan_refs(str_va, name, win=0x800):
    page = str_va & ~0xFFF
    off = str_va - page
    found = []
    for lo, hi in [(0x0, 0x10022b8), (0x1574000, len(d)-8)]:
        for o in range(lo, hi-4, 4):
            w1 = struct.unpack_from('<I', d, o)[0]
            if (w1 & 0x9F000000) == 0x90000000:
                rd = w1 & 0x1F
                imm = ((w1 >> 5) & 0x7FFFF) << 12
                if ((o & ~0xFFF) + imm) == page:
                    for j in range(o+4, min(o+win, hi-4), 4):
                        w2 = struct.unpack_from('<I', d, j)[0]
                        if (w2 & 0x1F) != rd: continue
                        if (w2 & 0xFFC00000) == 0x91000000:  # add
                            off2 = (w2 >> 10) & 0xFFF
                            if off2 == off:
                                found.append((o, j, 'add'))
                        elif (w2 & 0xFFC00000) == 0xF9400000:  # ldr
                            off2 = ((w2 >> 10) & 0xFFF) << 3
                            if off2 == off:
                                found.append((o, j, 'ldr'))
    print(f"[{name}] {str_va:#x}: {len(found)} 引用")
    for a, b, t in found:
        print(f"    adrp@{a:#x} {t}@{b:#x}")
    return found

scan_refs(0xdebaa8, "certificate verify failed (SSL_R_)")
scan_refs(0xdc61d0, "x509_vfy.c 文件串")