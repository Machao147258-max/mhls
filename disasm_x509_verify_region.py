# -*- coding: utf-8 -*-
"""反汇编 0xbc9b00-0xbca500, 回溯 X509_verify_cert 真实入口, 找函数序言与边界"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    return None

START, END = 0xbc9800, 0xbca800
code = d[v2off(START):v2off(END)]
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# 标记字符串引用点
mark = {0xbc9fb0:'adrp^unsupported purpose', 0xbc9ff8:'adrp^unable local issuer',
        0xbca010:'adrp^self signed', 0xbca070:'adrp^expired', 0xbca094:'adrp^sig failure'}
mark_addr = set(mark)

for ins in md.disasm(code, START):
    tag = ''
    if ins.address in mark_addr:
        tag = f'    <<<< {mark[ins.address]}'
    print(f"{hex(ins.address)}: {ins.mnemonic:8s} {ins.op_str}{tag}")