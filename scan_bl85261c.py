# -*- coding: utf-8 -*-
# 全文件分块扫描 bl→0x85261c
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

rt = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so', 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True
T = 0x85261c
calls = []
for start in range(0, len(rt), 0x100000):
    chunk = rt[start:start + 0x100000]
    for ins in md.disasm(chunk, start):
        if ins.mnemonic == 'bl' and ins.operands:
            if ins.operands[0].imm == T:
                calls.append(ins.address)
print('bl->0x85261c 调用者:', len(calls))
for a in calls[:30]:
    print(f'   0x{a:x}')
