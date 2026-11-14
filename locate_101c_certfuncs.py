# -*- coding: utf-8 -*-
"""libcocos2dlua.so (1.0.1c) 证书校验函数定位: 错误字符串 -> xref -> 函数入口
   策略: .rodata 找 1.0.1c 特有证书错误串, 在代码段搜 ADRP xN, #page + ADD xN,xN,#pageoff
         引用者即错误产生点(函数体内), 回溯到函数入口"""
from capstone import *
from capstone.arm64 import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None
def off2v(o):
    if 0 <= o < 0x10022b8: return o
    if 0x1002e08 <= o < 0x1580540: return o + 0x10000
    if 0x1574000 <= o < 0x1906000: return o + 0x3d000
    return None

# 1.0.1c 证书/握手错误串 (ssl/s3_clnt.c, crypto/x509/x509_vfy.c)
strings_101 = [
    b'no certificate returned',
    b'wrong signature length in certificate',
    b'bad signature',
    b'no shared cipher',
    b'server certificate type not supported',
    b'certificate verify failed',
    b'unable to get local issuer certificate',
    b'unable to get issuer certificate',
    b'self signed certificate',
    b'certificate has expired',
    b'unknown ca',
    b'unable to get certificate CRL',
    b'invalid CA certificate',
    b'unsupported certificate purpose',
    b'unsupported certificate signature algorithm',
    b'certificate signature failure',
    b'chain length too short',
    b'certificate not yet valid',
    b'EE certificate key too weak',
    b'CA certificate key too weak',
]

print("=== 字符串命中 ===")
strlocs = {}
for s in strings_101:
    hits = []
    start = 0
    while True:
        i = d.find(s, start)
        if i < 0: break
        v = off2v(i)
        if v is not None:
            hits.append(v)
        start = i + 1
    if hits:
        strlocs[s] = hits
        print(f"  {s.decode('ascii','replace'):48s} -> {[hex(h) for h in hits]}")

# 代码段: 0x100000-0x10022b8 (LOAD0 RX) 与 0x15b1000-0x1906000 (LOAD2 RX) 均反汇编成本高
# 更聪明: 只在 DATA 附近找引用。先拿一个字符串做 xref 验证方法。
CODE_LO, CODE_HI = 0x100000, 0x10022b8
CODE2_LO, CODE2_HI = 0x15b1000, 0x1906000

def find_adrp_add(rodata_vaddr):
    """在代码段找 ADRP+ADD 组合引用 rodata_vaddr (返回引用指令地址列表)"""
    page = rodata_vaddr & ~0xFFF
    off = rodata_vaddr & 0xFFF
    refs = []
    for lo, hi in [(CODE_LO, CODE_HI), (CODE2_LO, CODE2_HI)]:
        code = d[v2off(lo):v2off(hi)]
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        md.skipdata = True
        for ins in md.disasm(code, lo):
            if ins.mnemonic == 'adrp':
                # adrp xN, #page  -- imm 是 page 地址
                try:
                    imm = int(ins.op_str.split('#')[-1], 0)
                except Exception:
                    continue
                if imm == page:
                    refs.append(ins.address)
    return refs

# 测试一个字符串做 xref
if strlocs:
    s = list(strlocs.keys())[0]
    v = strlocs[s][0]
    print(f"\n=== xref 测试: {s.decode()} @ {hex(v)} ===")
    refs = find_adrp_add(v)
    print(f"引用者(adrp): {[hex(r) for r in refs]}")
    # 对每个 adrp 地址再找后续 8 条指令中的 add xN,xN,#off
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    for r in refs:
        code = d[v2off(r):v2off(r)+64]
        for ins in md.disasm(code, r):
            if ins.mnemonic == 'add':
                print(f"  {hex(ins.address)}: {ins.mnemonic} {ins.op_str}   <- 引用 {hex(v)}")
                break