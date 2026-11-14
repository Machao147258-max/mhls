# -*- coding: utf-8 -*-
"""libcocos2dlua.so: 定位 OpenSSL 1.0.1c 版本字符串, 用 xref 锚定代码区间"""
import subprocess

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

# LOAD0 offset==vaddr; LOAD1 vaddr=off+0x10000; LOAD2 vaddr=off+0x3d000
def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

probes = [b'OpenSSL 1.0.1', b'OpenSSL 1.', b'10 May 2012', b'built on:',
          b'TLSv1', b'SSLv3', b'SSLv2', b'TLSv1.1', b'TLSv1.2', b'SSL_accept',
          b'error:1409', b'14094410']
for p in probes:
    idxs = []
    start = 0
    while True:
        i = d.find(p, start)
        if i < 0: break
        idxs.append(i)
        start = i + 1
    print(f"{p.decode('ascii','replace'):20s} -> {len(idxs)} hits: {[hex(i) for i in idxs[:6]]}")

# 找出 "OpenSSL 1.0.1c" 的确切串和周围 rodata
i = d.find(b'OpenSSL 1.0.1')
if i >= 0:
    print("\n--- rodata context @", hex(i), "---")
    print(d[i-64:i+192].decode('ascii', 'replace').replace('\x00', '|'))
    # 该串 vaddr
    if i < 0x10022b8:
        print("vaddr =", hex(i))