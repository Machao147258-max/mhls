# -*- coding: utf-8 -*-
"""1) 搜 'x509_vfy.c' / 's3_clnt.c' / 'ssl_verify' 等串位置
2) 反汇编 0xbc9800~0xbc9df8 (X509_verify_cert_error_string 前方区域 = x509_vfy.c 同单元)
3) 反汇编 0xbc9250~0xbc9800 补齐中间区"""
import struct, re
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("========== 1) 关键字符串位置 ==========")
for s in [b'x509_vfy.c', b'x509_lu.c', b'x509_v3.c', b's3_clnt.c', b's3_srvr.c', b'verify error', b'certificate verify']:
    idxs = [m.start() for m in re.finditer(re.escape(s), d)]
    print(f"  {s.decode():25s}: {[hex(i) for i in idxs[:10]]}")

print("\n========== 2) 反汇编 0xbc9800~0xbc9df8 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc9800:0xbc9df8], 0xbc9800):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")