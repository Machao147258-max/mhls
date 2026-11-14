# -*- coding: utf-8 -*-
"""反汇编 0x3cd8a8 函数周边: 只打印 cmp/b/tbz/tbnz/bl 关键指令"""
from capstone import *
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True
KEY = ('cmp', 'b.', 'tbz', 'tbnz', 'bl', 'cbz', 'cbnz', 'ldrb', 'strb', 'mov', 'add', 'sub')
lo, hi = 0x3cd800, 0x3cda80
cnt = 0
for ins in md.disasm(d[lo:hi], lo):
    if ins.mnemonic.startswith(KEY) or ins.mnemonic in ('b', 'br', 'blr'):
        print(f"{ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        cnt += 1
        if cnt > 120: break
print("...total shown", cnt)