# -*- coding: utf-8 -*-
"""
《猫和老鼠》com.netease.tom SSL/TLS 证书校验绕过 — 静态 patch 生成器
目标库: lib_arm64/tom_lib/libAudioCommon.so (内嵌 OpenSSL 1.1.1q, 符号明文可信)
方法:   将 5 个证书校验函数入口覆写为 'mov w0,#1; ret' (AArch64)
        X509_verify_cert / ssl_verify_cert_chain / tls_process_server_certificate
        / ssl3_check_cert_and_algorithm / X509_check_host
输出:   libAudioCommon.so.patched  +  SHA1 校验清单 (此前 5 点函数序言已逐一验证为标准 Prologue)
用法:   python patch_openssl.py
"""
import os, hashlib, sys, shutil

BASE = r'C:\Users\20751\Desktop\猫和老鼠'
SRC  = os.path.join(BASE, r'lib_arm64\tom_lib\libAudioCommon.so')
DST  = os.path.join(BASE, r'lib_arm64\tom_lib\libAudioCommon.so.patched')

# 函数入口 -> 期望当前序言(前8字节) -> 描述
PATCHES = [
    (0x2a2dd4, 'f6 57 bd a9 f4 4f 01 a9', 'X509_verify_cert (OpenSSL 1.1.1q 证书链验证核心)'),
    (0x212894, 'f6 57 bd a9 f4 4f 01 a9', 'ssl_verify_cert_chain (SSL 握手期证书链校验入口)'),
    (0x22b450, 'ff c3 01 d1 f9 13 00 f9', 'tls_process_server_certificate (TLS1.2/1.3 服务端证书处理)'),
    (0x22cdec, 'f5 0f 1d f8 f4 4f 01 a9', 'ssl3_check_cert_and_algorithm (证书类型/算法检查)'),
    (0x2b7e6c, 'f7 0f 1c f8 f6 57 01 a9', 'X509_check_host (hostname 校验; 若业务启用 SSL_set1_host 需一并绕过)'),
]

MOV_W0_1_RET = bytes.fromhex('20 00 80 52 C0 03 5F D6')   # mov w0,#1 ; ret

def sha1(path):
    h = hashlib.sha1()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(1 << 20), b''):
            h.update(chunk)
    return h.hexdigest()

def main():
    if not os.path.exists(SRC):
        print(f'[!] source not found: {SRC}'); sys.exit(1)
    data = bytearray(open(SRC, 'rb').read())
    orig_sha = sha1(SRC)
    print(f'[i] source : {SRC}')
    print(f'[i] size   : {hex(len(data))}')
    print(f'[i] sha1   : {orig_sha}')
    print()

    patched = []
    for va, expect_hex, desc in PATCHES:
        expect = bytes.fromhex(expect_hex)
        if data[va:va+8] != expect:
            print(f'[!] MISMATCH @0x{va:x}: {data[va:va+8].hex(" ")} != {expect_hex}  ({desc})')
            print(f'    (符号可能被混淆偏移, 跳过以保安全)')
            continue
        data[va:va+8] = MOV_W0_1_RET
        patched.append((va, desc))
        print(f'[+] {desc:58s} @0x{va:x}: {expect_hex} -> 20 00 80 52 C0 03 5F D6')

    if not patched:
        print('[x] 无有效 patch 点, 终止'); sys.exit(2)

    open(DST, 'wb').write(data)
    print()
    print(f'[i] patched : {DST}')
    print(f'[i] new sha1: {sha1(DST)}')
    with open(os.path.join(BASE, 'patch_manifest.txt'), 'w') as f:
        f.write(f'source_sha1: {orig_sha}\n')
        f.write(f'patched_sha1: {sha1(DST)}\n')
        f.write(f'patch_bytes: {MOV_W0_1_RET.hex()}\n')
        for va, desc in patched:
            f.write(f'0x{va:x}: {desc}\n')
    print('[i] manifest written: patch_manifest.txt')

if __name__ == '__main__':
    main()