# -*- coding: utf-8 -*-
"""1) dump 0xdc6140~0xdc6320 全部字符串 (文件串归属实证)
2) 完整反汇编 0xbc93a8~0xbc9568
3) 确认 FUNC 0x92/0x91 对应的 X509_F_ 常量名 (从 .symtab/.dynsym 或 err 数据)"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("========== 1) 0xdc6140~0xdc6320 字符串 ==========")
off = 0xdc6140
end = 0xdc6320
i = off
while i < end:
    if 32 <= d[i] < 127:
        j = i
        while j < end and 32 <= d[j] < 127:
            j += 1
        s = d[i:j].decode('ascii', 'replace')
        if len(s) >= 3:
            print(f"  {i:#x}: '{s}'")
        i = j
    else:
        i += 1

print("\n========== 2) 完整反汇编 0xbc93a8~0xbc9568 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc93a8:0xbc9568], 0xbc93a8):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")