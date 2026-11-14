# -*- coding: utf-8 -*-
"""扫描 bl -> 0xbc9df8 (X509_verify_cert_error_string) 的调用者 => X509_verify_cert 主体"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

TGT = 0xbc9df8
CODE_REGIONS = [(0x0, 0x10022b8), (0x15b1000, 0x1906000)]
CHUNK = 0x8000

callers = set()
for lo, hi in CODE_REGIONS:
    cur = lo
    while cur < hi:
        n = min(CHUNK, hi - cur)
        code = d[cur:cur+n]
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        md.skipdata = True
        try:
            for ins in md.disasm(code, cur):
                if ins.mnemonic == 'bl':
                    try:
                        tgt = int(ins.op_str, 16)
                    except Exception:
                        tgt = None
                    if tgt == TGT:
                        callers.add(ins.address)
        except CsError:
            pass
        cur += n

print(f"== {len(callers)} 个 bl -> X509_verify_cert_error_string 调用点 ==")
for a in sorted(callers):
    print(f"  bl {TGT:#x} @ {a:#x}")

# 对调用者附近反汇编找函数边界 (向前找序言 stp x29, x30)
print("\n== 调用者所在函数边界探测 ==")
def is_prologue(addr):
    if addr < 0 or addr >= len(d): return False
    # stp x29, x30, [sp, #-N]!  -> 0xfd 0x7b bf a9 (小端) / 常见 4 字节: FD 7B BF A9 / F6 57 BD A9 等
    b = d[addr:addr+4]
    return b in (bytes.fromhex('fd7bbfa9'), bytes.fromhex('f657bda9'), bytes.fromhex('ff8301d1')) or b[0] in (0xfd, 0xf6, 0xf8)

import struct
for a in sorted(callers):
    # 向前最多 0x3000 找序言
    found = None
    for back in range(0, 0x3000, 4):
        if is_prologue(a - back):
            found = a - back
            break
    print(f"  调用点 {a:#x} -> 函数入口疑似 {found:#x if found else '?'}")