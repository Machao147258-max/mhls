# -*- coding: utf-8 -*-
"""定位 X509_verify_cert / ssl_verify_cert_chain 调用链:
thunk 区 [0xbc9fb0, 0xbca098] 是引用证书错误串的 12B 参数搬运序列,
扫描全代码段 bl 目标落在 thunk 区的调用者 -> 证书校验函数本体"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

THUNK_LO, THUNK_HI = 0xbc9fb0, 0xbca098 + 0x200
CODE_REGIONS = [(0x0, 0x10022b8), (0x15b1000, 0x1906000)]
CHUNK = 0x8000

callers = set()   # (bl_addr, target)
for lo, hi in CODE_REGIONS:
    cur = lo
    while cur < hi:
        n = min(CHUNK, hi - cur)
        code = d[v2off(cur):v2off(cur)+n]
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        md.skipdata = True
        try:
            for ins in md.disasm(code, cur):
                if ins.mnemonic in ('bl', 'blr'):
                    # 立即目标
                    tgt = None
                    try:
                        if ins.mnemonic == 'bl':
                            tgt = int(ins.op_str, 16)
                    except Exception:
                        tgt = None
                    if tgt and THUNK_LO <= tgt <= THUNK_HI:
                        callers.add((ins.address, tgt))
        except CsError as e:
            print(f"chunk err @ {hex(cur)}: {e}")
        cur += n

print(f"== {len(callers)} 个调用者 bl -> thunk 区 ==")
by_caller = {}
for a, t in sorted(callers):
    by_caller.setdefault(a, []).append(t)
    print(f"  bl {t:#x}  @ {a:#x}")

# 调用者聚集 -> 推断函数边界 (找调用者前后最近的序言)
print("\n== 调用者聚集分布 ==")
addrs = sorted(by_caller.keys())
for a in addrs:
    print(f"  {a:#x}")