# -*- coding: utf-8 -*-
"""交叉验证 libAudioCommon.so (OpenSSL 1.1.1q) 4 个证书校验 patch 点当前字节 + 检查字符串/错误码特征"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so'
d = open(F, 'rb').read()
print("libAudioCommon.so size:", hex(len(d)))

# ELF program headers (offset/vaddr)
import subprocess
r = subprocess.run(['readelf', '-l', F], capture_output=True, text=True)
for ln in r.stdout.splitlines():
    if 'LOAD' in ln and '0x' in ln:
        print(ln)

def v2off(v):
    # 由 program headers 反推 (此处先按 lo 段 vaddr==offset 处理, 若超范围再修正)
    return v

# patch 点 (此前已确认)
PATCHES = {
    'X509_verify_cert':         0x2a2dd4,
    'ssl_verify_cert_chain':    0x212894,
    'tls_process_server_certificate': 0x22b450,
    'ssl3_check_cert_and_algorithm':  0x22cdec,
    'X509_check_host':          0x2b7e6c,
}
MOV_W0_1 = bytes.fromhex('20 00 80 52')   # mov w0,#1
MOV_W0_1_RET = bytes.fromhex('20 00 80 52 C0 03 5F D6')

print("\n=== patch 点字节 ===")
for name, v in PATCHES.items():
    off = v2off(v)
    cur = d[off:off+8]
    print(f"  {name:38s} @ {hex(v)}: {cur.hex(' ')}")

# 错误字符串: 1.1.1q 证书验证错误串
probes = [b'certificate verify failed', b'ee key too small', b'unsupported certificate purpose',
          b'certificate has expired', b'self signed certificate', b'X509_verify_cert',
          b'SSL_CTX_set_keylog_callback', b'keylog', b'pinned', b'Pinned', b'Public Key Pinning']
for p in probes:
    n = d.count(p)
    print(f"  {p.decode('ascii','replace'):45s} x{n}")

# SSL_CTX_set_keylog_callback 是否被调用: 找 GOT 引用
r = subprocess.run(['readelf', '-rW', F], capture_output=True, text=True)
for ln in (r.stdout or '').splitlines():
    if 'keylog' in ln or 'SSL_CTX_set_' in ln:
        print("RELOC:", ln.strip()[:150])