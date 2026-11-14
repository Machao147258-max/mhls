# -*- coding: utf-8 -*-
"""1) 完整反汇编 0xbc93a8~0xbc9800 (疑似 X509_verify_cert)
2) 搜索 ERR 函数名字符串 (X509_F_*) 确认 FUNC 码
3) 读 0xdc6228 附近字符串"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

print("========== 1) 反汇编 0xbc93a8~0xbc9800 ==========")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
for ins in md.disasm(d[0xbc93a8:0xbc9800], 0xbc93a8):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n========== 2) 搜索 X509_F_ 函数名字符串 ==========")
import re
for m in re.finditer(rb'X509_F_[A-Z0-9_]{5,60}', d):
    s = m.group().decode()
    if 'VERIFY' in s or 'CHAIN' in s or 'SUBJECT' in s or 'CHECK' in s:
        print(f"  @ {m.start():#x}: {s}")

print("\n========== 3) 0xdc6228 附近字符串 ==========")
for off in range(0xdc6210, 0xdc6320, 1):
    if d[off] == 0:
        continue
    # 连续可打印串
    s = d[off:off+60].split(b'\x00')[0]
    if all(32 <= c < 127 for c in s) and len(s) > 8:
        print(f"  {off:#x}: '{s.decode()}'")