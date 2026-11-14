# -*- coding: utf-8 -*-
"""libcocos2dlua.so (1.0.1c): 定位 SSL_METHOD 实际方法表 (TLSv1_client_method / SSLv23_client_method)
   方法: 在可写数据段中搜索 ssl-aware 函数指针数组特征
   已知锚点: ssl3_undef_enc_method@0x157ee90 (空表), ssl3_ciphers@0x157bc48,
            SSL_accept(包装)@0xc8d6cc = method->ssl_accept 间接调用?
   实际 SSL_METHOD 表 (如 ssl3_0_2_0 静态/ ssl3_method 等) 会含 ssl3_version_str/d tls1_enc_data 指针"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def voff(v):
    if 0x0 <= v < 0x10022b8:   return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

# 可疑 SSL_METHOD 表: 结构应为 20+ qwords, 其中 [1]=ssl_new(可执行区) [4]=ssl_accept [5]=ssl_connect [6]=ssl_read [8]=ssl_write
# ssl3_enc_method 指针(即 TLSv1_enc_data: 10 个函数指针, 221字节组) 位于表末
RW_LO, RW_HI = 0x1012e08, 0x1580540   # LOAD1 (RW) vaddr
exec_set = {(0, 0x10022b8), (0x15b1000, 0x1906000)}

def in_exec(v):
    for lo, hi in exec_set:
        if lo <= v < hi:
            return True
    return False

cands = []
# 以 8 对齐扫描 RW 段
for v in range(RW_LO + 8, RW_HI - 22*8, 8):
    q = struct.unpack_from('<22Q', d, voff(v))
    # [1]=ssl_new 指向可执行, [4]/[5] 之一也指向可执行, 且 version 字段小整数
    version = q[0]
    if not (0 < version < 0x400):
        continue
    if not (in_exec(q[1]) and (in_exec(q[4]) or in_exec(q[5]))):
        continue
    score = 0
    for idx in (2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21):
        if in_exec(q[idx]):
            score += 1
    if score >= 6:
        cands.append((v, version, q, score))

print(f"候选 SSL_METHOD 表: {len(cands)}")
for v, ver, q, sc in cands[:12]:
    print(f"  vaddr={hex(v)} version={ver} score={sc}")
    print(f"    new={hex(q[1])} clear={hex(q[2])} free={hex(q[3])} accept={hex(q[4])} connect={hex(q[5])}")
    print(f"    read={hex(q[6])} peek={hex(q[7])} write={hex(q[8])} shutdown={hex(q[9])}")
    print(f"    pending={hex(q[12])} num_ciphers={hex(q[13])} get_cipher={hex(q[14])} default_timeout={hex(q[15])}")
    print(f"    ssl3_enc={hex(q[16])} version_f={hex(q[17])} ctrl={hex(q[18])}")