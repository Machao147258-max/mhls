# -*- coding: utf-8 -*-
"""最终验证: 1) capstone 解码 patched 区 2) 备份存在性 3) 引用者汇总"""
import os, struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
BAK = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so.orig'
d = open(F, 'rb').read()

print("=== 1) patched 区解码 (0xbc5e4c ~ 0xbc5e60) ===")
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
for ins in md.disasm(d[0xbc5e4c:0xbc5e60], 0xbc5e4c):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== 2) 备份 ===")
print(f"  .orig 存在: {os.path.exists(BAK)}, 大小 {os.path.getsize(BAK) if os.path.exists(BAK) else 0}")

print("\n=== 3) X509_verify_cert 调用者汇总 ===")
print("  0xbc72f0  (X509 层包装)")
print("  0xbd9d34  (X509 层包装)")
print("  0xc80ff8  (SSL 层 ssl_verify_cert_chain 路径1)")
print("  0xc88ad4  (SSL 层 ssl_verify_cert_chain 路径2)")
print("  0xc8f05c  (SSL 层 ssl_verify_cert_chain 默认路径, 即 app_verify_callback==NULL)")

print("\n=== 4) ssl_verify_cert_chain 本体 0xc8ef60 ===")
for ins in md.disasm(d[0xc8ef60:0xc8f018], 0xc8ef60):
    if ins.mnemonic in ('bl','blr','cbz','cbnz','b','ret'):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")

print("\n=== 5) 文件校验和 ===")
import hashlib
print(f"  patched MD5: {hashlib.md5(d).hexdigest()}")
if os.path.exists(BAK):
    print(f"  orig   MD5: {hashlib.md5(open(BAK,'rb').read()).hexdigest()}")