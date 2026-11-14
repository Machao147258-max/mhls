# -*- coding: utf-8 -*-
"""验证 libcocos2dlua.so FUNC 符号 Value 是否可信:
   1) BIO_puts@0xba34fc (272B) 应为 strlen+尾调 BIO_write
   2) X509_STORE_CTX_get_error_depth@0xbc57a0 (8B) 应为 单 ldr + ret
   3) BN_exp / BN_rand 也抽查
   若这些标准函数反汇编正常 -> FUNC 部分可信 (SSL_accept 那个是巧合?); 若乱 -> FUNC 全部不可信"""
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)

def dis(v, n):
    off = v2off(v)
    code = d[off:off+n]
    for ins in md.disasm(code, v):
        print(f"  {hex(ins.address)}: {ins.mnemonic:8s} {ins.op_str}")

checks = [
    ('BIO_puts', 0xba34fc, 0x110),          # 272B
    ('X509_STORE_CTX_get_error_depth', 0xbc57a0, 0x10),
    ('OBJ_NAME_remove', 0xbeb858, 0xA4),
    ('BN_exp', 0xbf867c, 0x1BC),
    ('BN_rand', 0xbfd3ec, 0x1DC),
    ('RAND_poll', 0xc1ce5c, 0x284),
    ('SSL_get_srtp_profiles', 0xc894fc, 0x30),
    ('dtls1_listen', 0xc96f88, 0x70),
]
for name, v, n in checks:
    print(f"\n===== {name} @ {hex(v)} ({n}B) =====")
    dis(v, min(n, 0x80))