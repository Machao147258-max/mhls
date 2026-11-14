# -*- coding: utf-8 -*-
"""libepay-crypto.so: 扫描 .text 中 adrp/add 引用 .rodata 方法名(0xa9bea/0xa9bcc等)"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True

# 目标字符串 VA
want = {0xa9bea: 'getAesKey', 0xa9bcc: 'getFlexibleSecret', 0xa9c13: 'base64Encode', 0xa9c20: 'base64Decode'}
# adrp 的 imm12 是页偏移 (<<12)
def adrp_target(ins):
    # op_str like 'x0, #0xa9000'
    try:
        off = int(ins.op_str.split('#')[1].replace(',',''), 0)
        return off
    except Exception:
        return None

text_lo, text_hi = 0x408b0, 0x408b0 + 0x6903c
hits = []
seq = list(md.disasm(d[text_lo:text_hi], text_lo))
for i, ins in enumerate(seq):
    if ins.mnemonic == 'adrp':
        base = adrp_target(ins)
        if base is None: continue
        # 找后续 2-4 条内的 add x?, x?, #imm (imm12, 页内偏移)
        for j in range(i+1, min(i+5, len(seq))):
            s2 = seq[j]
            if s2.mnemonic == 'add':
                try:
                    imm = int(s2.op_str.split('#')[-1], 0)
                except Exception:
                    continue
                addr = base + imm
                if addr in want:
                    hits.append((ins.address, want[addr]))
                    break
for a, name in hits:
    print("  %#x 引用 %s" % (a, name))

print("命中 %d 处" % len(hits))