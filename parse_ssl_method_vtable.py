# -*- coding: utf-8 -*-
"""解析 libcocos2dlua.so (OpenSSL 1.0.1c) 的 SSL_METHOD vtable, 获取被混淆核心函数真实地址"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

# vaddr -> file offset (via program headers)
def voff(v):
    if 0x0 <= v < 0x10022b8:   return v              # LOAD0 R E (offset==vaddr)
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000  # LOAD1 RW (offset=vaddr-0x10000)
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000  # LOAD2 R E (offset=vaddr-0x3d000)
    return None

# ssl3_undef_enc_method @ 0x157ee90 (112B) - 14 qwords
base = 0x157ee90
off = voff(base)
print(f"ssl3_undef_enc_method vaddr={hex(base)} fileoff={hex(off)}")
q = struct.unpack_from('<14Q', d, off)
for i, v in enumerate(q):
    print(f"  [{i:2d}] {hex(v)}")

# SSL_METHOD layout (1.0.1): 0:version(int) 1:ssl_new 2:ssl_clear 3:ssl_free
# 4:ssl_accept 5:ssl_connect 6:ssl_read 7:ssl_peek 8:ssl_write 9:ssl_shutdown
names = {1:'ssl_new',2:'ssl_clear',3:'ssl_free',4:'ssl_accept',5:'ssl_connect',
         6:'ssl_read',7:'ssl_peek',8:'ssl_write',9:'ssl_shutdown'}
print("\n=== SSL_METHOD 函数指针 ===")
for i, v in enumerate(q):
    if i in names and v:
        print(f"  {names[i]:14s} @ {hex(v)}")

# 验证 ssl3_accept 与已知 SSL_accept@0xc8d6cc 关系
print(f"\n[verify] SSL_accept(包装)@0xc8d6cc (84B) vs vtable ssl_accept={hex(q[4])}")