# -*- coding: utf-8 -*-
"""反汇编 0xbc9800~0xbca140 (错误分支区+函数入口) 与 0xc26000~0xc26100 (公共错误处理)"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def disasm(va, size, label):
    print(f"\n===== {label}: {va:#x} (+{size:#x}) =====")
    md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    md.skipdata = True
    code = d[va:va+size]
    count = 0
    for ins in md.disasm(code, va):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        count += 1
    print(f"  ({count} ins)")

# 1) 错误分支区 + 前方函数入口
disasm(0xbc9800, 0xbc9fb0-0xbc9800, "函数入口区(错误分支前)")
disasm(0xbc9fb0, 0xbca140-0xbc9fb0, "错误分支区")

# 2) 公共错误处理
disasm(0xc26000, 0x120, "公共错误处理 @0xc26038 附近")