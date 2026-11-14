# -*- coding: utf-8 -*-
"""分块 ADRP+ADD xref: 定位引用证书错误串的代码 -> 回溯函数入口"""
from capstone import *
from capstone.arm64 import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

RODATA_TARGETS = {
    0xdebaa8: 'certificate verify failed',
    0xdc6508: 'unable to get local issuer certificate',
    0xdc64c0: 'self signed certificate',
    0xdc6660: 'unsupported certificate purpose',
    0xdc6378: 'certificate signature failure',
    0xdec3c0: 'no certificate returned',
    0xdec5c0: 'no shared cipher',
    0xdc63e8: 'certificate has expired',
}
pages = {v & ~0xFFF: v for v in RODATA_TARGETS}
page_to_str = {}
for v, s in RODATA_TARGETS.items():
    page_to_str[v & ~0xFFF] = (v, s)

CODE_REGIONS = [(0x100000, 0x10022b8), (0x15b1000, 0x1906000)]
CHUNK = 0x10000

found = {}   # str -> list of (adrp_addr, add_addr, reg)
for lo, hi in CODE_REGIONS:
    cur = lo
    while cur < hi:
        n = min(CHUNK, hi - cur)
        code = d[v2off(cur):v2off(cur)+n]
        md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
        md.skipdata = True
        try:
            for ins in md.disasm(code, cur):
                if ins.mnemonic != 'adrp':
                    continue
                try:
                    imm = int(ins.op_str.split('#')[-1], 0)
                except Exception:
                    continue
                if imm in page_to_str:
                    vidx = imm
                    # 在该 adrp 后 12 条指令找 add xN,xN,#offset
                    add_off = ins.address - cur
                    tail = code[add_off:add_off+64]
                    for ins2 in md.disasm(tail, ins.address):
                        if ins2.mnemonic == 'add':
                            ops = ins2.op_str
                            rreg = ins.op_str.split(',')[0].strip()
                            if ops.startswith(rreg + ','):
                                tgt = imm + (int(ops.split('#')[-1], 0) & 0xFFF)
                                if tgt in RODATA_TARGETS:
                                    s = RODATA_TARGETS[tgt]
                                    found.setdefault(s, []).append((ins.address, ins2.address))
                                    print(f"  [+] {s} @ {hex(tgt)} <- adrp {hex(ins.address)}, add {hex(ins2.address)}")
                            break
        except CsError as e:
            print(f"  chunk err @ {hex(cur)}: {e}")
        cur += n

print(f"\n=== 引用汇总 ===")
for s, refs in found.items():
    print(f"  {s}: {len(refs)} 处")
    for a, b in refs:
        print(f"      {hex(a)} -> {hex(b)}")