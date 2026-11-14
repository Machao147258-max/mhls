# -*- coding: utf-8 -*-
"""1) 反汇编 0xbc4364 区域 (0xbc4200~0xbc4c00)
2) 字节级搜 add xN,xN,#0x1d0 (opcode=0x91000000|(0x1d0<<10)|Rn<<5|Rd) 全代码区 -> 加载 0xdc61d0 x509_vfy.c
3) objdump -t 查 X509/verify 符号
4) 反汇编 0xbca098~0xbca500 (error_string case 区之后)"""
import struct, subprocess
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("========== 1) 反汇编 0xbc4200~0xbc4c00 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc4200:0xbc4c00], 0xbc4200):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n========== 2) add xN,xN,#0x1d0 全代码区 ==========")
opc_base = 0x91000000 | (0x1d0 << 10)
hits = []
for lo, hi in [(0x0, 0x10022b8), (0x1574000, len(d)-4)]:
    for o in range(lo, hi, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFFFFFC00) == opc_base and ((w >> 5) & 0x1F) == (w & 0x1F):
            hits.append(o)
print(f"  命中 {len(hits)} 处: {[hex(h) for h in hits[:50]]}")

# 同时扫 add xN,xN,#0x228 (x509_lu.c 0xdc6228) 对照
opc228 = 0x91000000 | (0x228 << 10)
hits2 = []
for lo, hi in [(0x0, 0x10022b8), (0x1574000, len(d)-4)]:
    for o in range(lo, hi, 4):
        w = struct.unpack_from('<I', d, o)[0]
        if (w & 0xFFFFFC00) == opc228 and ((w >> 5) & 0x1F) == (w & 0x1F):
            hits2.append(o)
print(f"  add #0x228(x509_lu.c) 命中 {len(hits2)} 处: {[hex(h) for h in hits2[:50]]}")

print("\n========== 3) objdump -t X509 符号 ==========")
try:
    r = subprocess.run(['objdump', '-t', F], capture_output=True, text=True, errors='replace')
    for ln in r.stdout.split('\n'):
        if any(k in ln for k in ['X509_verify_cert', 'internal_verify', 'check_issued',
                                 'X509_STORE_CTX_verify', 'ssl_verify_cert_chain', 'X509_STORE_CTX_init']):
            print(f"  {ln.strip()}")
except Exception as e:
    print(f"  err {e}")

print("\n========== 4) 反汇编 0xbca098~0xbca500 ==========")
md2 = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md2.skipdata = True
for ins in md2.disasm(d[0xbca098:0xbca500], 0xbca098):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")