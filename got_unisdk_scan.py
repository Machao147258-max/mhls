# -*- coding: utf-8 -*-
"""1) 全文件扫 GOT 间接调用 (LDR x8,[addr]+BLR x8) 引向 SSL_CTX_new 等
   2) 检查易盾/unisdk 库内部的 OpenSSL 特征"""
import struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so"
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# GOT 表在 ELF 动态段 - 找到 .got 段位置 (RW 段)
# 简化: 直接查符号地址附近的 GOT 引用 - 用 objdump -R (reloc) 更准确
import subprocess
r = subprocess.run(["readelf", "-r", SO], capture_output=True, timeout=120)
rtxt = (r.stdout or b'').decode('utf-8', 'replace')
print("=== RELA (GOT/PLT) 关键项 ===")
for ln in rtxt.splitlines():
    if re_search := __import__('re').search(r'(SSL_CTX_new|SSL_new|SSL_read\b|SSL_write\b|SSL_connect\b|SSL_do_handshake|BIO_read|BIO_write|ssl_verify_cert_chain|X509_verify_cert)', ln):
        print(" ", ln.strip()[:160])

print("\n=== 易盾库 OpenSSL 特征 ===")
for fn in ["libunisec.so", "unisec.so", "secsdk.so", "libsec-lib.so", "libybuaxz.so"]:
    p = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib" + "\\" + fn
    try:
        d = open(p, 'rb').read()
    except Exception as e:
        print(fn, "ERR", e); continue
    markers = {
        "OpenSSL": d.count(b"OpenSSL"),
        "SSL_CTX_new": d.count(b"SSL_CTX_new"),
        "SSL_read": d.count(b"SSL_read"),
        "X509_verify_cert": d.count(b"X509_verify_cert"),
        "BEGIN CERT": d.count(b"-----BEGIN CERT"),
    }
    arch = "?"
    if d[:4] == b'\x7fELF':
        e_machine = struct.unpack_from('<H', d, 18)[0]
        arch = {183: 'x86_64', 62: 'x86', 183: 'x86_64', 40: 'ARM', 183: 'x86_64'}.get(e_machine, hex(e_machine))
        e_class = '64' if d[4] == 2 else '32'
        arch = f"{arch} ({e_class}bit ELF)"
    print(f"{fn:18s} {arch} size={len(d):>8d}")
    for k, v in markers.items():
        if v:
            print(f"     {k}: {v}")