# -*- coding: utf-8 -*-
"""扫描 lib_arm64/tom_lib 下所有 .so：
1. 是否含 OpenSSL(版本串/SSL_read 字符串) -> 判断 SSL 实现分布
2. 是否导出/定义 libcocos2dlua.so 中 8 个 UND 符号 -> 找提供者
3. 列出每个 so 的动态依赖(DT_NEEDED)用于加载顺序分析
"""
import os, re, struct

DIR = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib"
UND8 = [b"X509_STORE_set_default_paths", b"BIO_s_socket", b"X509_certificate_type",
        b"X509_STORE_load_locations", b"EVP_enc_null", b"OPENSSL_DIR_read",
        b"ERR_load_crypto_strings", b"OPENSSL_DIR_end"]

ssl_markers = [b"OpenSSL 1.0.1c", b"OpenSSL 1.1", b"BoringSSL", b"SSL_CTX_new", b"SSL_read"]
und_syms = set(UND8)

files = sorted(os.listdir(DIR))
for fn in files:
    if not fn.endswith('.so'):
        continue
    p = os.path.join(DIR, fn)
    data = open(p, 'rb').read()
    hits = []
    for m in ssl_markers:
        c = data.count(m)
        if c:
            hits.append(f"{m.decode()}:{c}")
    und_found = [u.decode() for u in und_syms if u in data]
    print(f"{fn:30s} {len(data):>9d}  SSL:{';'.join(hits) if hits else '-'}  UNDdef:{','.join(und_found) if und_found else '-'}")