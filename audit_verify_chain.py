# -*- coding: utf-8 -*-
"""1) ssl_verify_cert_chain 完整分支分析 (0xc8ef60~0xc8f040, 含 0xc8f01c init失败 & 0xc8f04c verify_mode)
2) 数据段扫描 qword 指针 -> 0xbc5e4c / 0xbc4a1c / 0xbc6a98 的指针表项"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("=== 1) ssl_verify_cert_chain 全分支 (0xc8ef60~0xc8f040) ===")
from capstone import *
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xc8ef60:0xc8f040], 0xc8ef60):
    mark = ''
    if ins.address in (0xc8f01c, 0xc8f04c, 0xc8f058): mark = '  <<<<'
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}{mark}")

print("\n=== 2) 数据段指针表 (qword == 目标地址) ===")
targets = {0xbc5e4c: 'X509_verify_cert', 0xbc4a1c: 'X509_STORE_CTX_verify_cert', 0xbc6a98: 'X509_STORE_CTX_init(魔改)', 0xc8ef60: 'ssl_verify_cert_chain'}
for lo, hi in [(0x10022bc, len(d)-8), (0x0, 0x10022b8)]:
    pass
lo, hi = 0x0, len(d)-8
hits = {}
for o in range(lo, hi-8, 8):
    v = struct.unpack_from('<Q', d, o)[0]
    if v in targets:
        hits.setdefault(v, []).append(o)
for v, addrs in hits.items():
    print(f"  {targets[v]} ({v:#x}): {len(addrs)} 处")
    for a in addrs[:20]:
        print(f"    @ {a:#x} (段: {'代码' if a < 0x10022b8 else ('数据' if a < 0x1574000+0x390000 else '其它')})")