# -*- coding: utf-8 -*-
"""1) .dynsym 查 X509_verify_cert 等符号 st_value
2) bl->0xbc93a8 扫描
3) s3_clnt.c (0xde9b40) / x509_vfy.c (0xdc61d0) 引用者宽窗口扫描
4) 反汇编 0xbc9568~0xbc9800"""
import struct, re
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("========== 1) dynsym 查符号 ==========")
# 用 objdump 提取
import subprocess
r = subprocess.run(['objdump', '-T', F], capture_output=True, text=True, errors='replace')
lines = r.stdout.split('\n')
for ln in lines:
    for name in ['X509_verify_cert', 'X509_STORE_CTX_get_by_subject', 'ssl_verify_cert_chain',
                 'ssl3_get_server_certificate', 'X509_check_issued', 'internal_verify',
                 'X509_STORE_CTX_verify', 'X509_STORE_CTX_verify_cert']:
        if name in ln:
            print(f"  {ln.strip()}")
            break

print("\n========== 2) bl -> 0xbc93a8 ==========")
hits = []
for lo, hi in [(0x0, 0x10022b8), (0x1574000, len(d)-4)]:
    for o in range(lo, hi, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFC000000) == 0x94000000:
            delta = w & 0x03FFFFFF
            if delta >= 0x02000000: delta -= 0x04000000
            if o + (delta << 2) == 0xbc93a8:
                hits.append(o)
print(f"  bl->0xbc93a8: {len(hits)} 处 {[hex(h) for h in hits]}")

print("\n========== 3) 字符串引用者宽窗口 ==========")
def find_refs(str_va, name):
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
                    # 同 rd 后续 add/ldr ±0x200
                    for j in range(o+4, min(o+0x200, hi-4), 4):
                        w2 = struct.unpack_from('<I', d, j)[0]
                        if (w2 & 0x1F) != rd: continue
                        if (w2 & 0xFFC00000) == 0x91000000:  # add imm
                            off2 = (w2 >> 10) & 0xFFF
                            if off2 == off: found.append((o, j, 'add'))
                        if (w2 & 0xFFC00000) == 0xF9400000:  # ldr
                            off2 = ((w2 >> 10) & 0xFFF) << 3
                            if off2 == off: found.append((o, j, 'ldr'))
    print(f"  {name} ({str_va:#x}): {len(found)} 引用")
    for a, b, t in found[:30]:
        print(f"    adrp@{a:#x} {t}@{b:#x}")
    return found

find_refs(0xde9b40, "s3_clnt.c")
find_refs(0xdc61d0, "x509_vfy.c")

print("\n========== 4) 反汇编 0xbc9568~0xbc9800 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc9568:0xbc9800], 0xbc9568):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")