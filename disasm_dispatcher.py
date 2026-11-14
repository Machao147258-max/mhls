# -*- coding: utf-8 -*-
"""反汇编 0xc8d560-0xc8d7c0: 确认 SSL_* 薄包装共享 dispatcher (method->fn 间接调用)"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

START, END = 0xc8d560, 0xc8d7c0
code = d[START:END]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

print(f"=== 0xc8d560-0xc8d7c0 (SSL wrapper 区域) ===")
for ins in md.disasm(code, START):
    print(f"{hex(ins.address)}: {ins.mnemonic:8s} {ins.op_str}")