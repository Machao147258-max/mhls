# -*- coding: utf-8 -*-
"""从 readelf -Ws 输出(UTF-16)解析 符号名(明文尾部) -> 地址 映射
识别: readelf 对混淆符号名显示 <XX> 转义前缀 + 明文后缀
"""
import re

FILE = r"C:\Users\20751\Desktop\猫和老鼠\elf_all_syms.txt"
OUT = r"C:\Users\20751\Desktop\猫和老鼠\sym_plain_map.txt"

raw = open(FILE, 'rb').read()
try:
    txt = raw.decode('utf-16')
except Exception:
    txt = raw.decode('utf-8', 'replace')

pat = re.compile(r'^\s*\d+:\s+([0-9a-fA-F]+)\s+(\d+)\s+(\S+)\s+(\S+)\s+\S+\s+(\S+)\s+(.*)$')
rows = []
for ln in txt.splitlines():
    m = pat.match(ln)
    if not m:
        continue
    addr = int(m.group(1), 16)
    size = int(m.group(2))
    typ = m.group(3)
    bind = m.group(4)
    ndx = m.group(5)
    name_part = m.group(6)
    # 提取明文后缀: 最后一段纯 ASCII 可打印 token(可能含 <XX> 转义前缀)
    # readelf 转义格式: <95><DD>...明文
    plain = ''
    toks = re.findall(r'[A-Za-z0-9_.~$:+\-\[\]]+', name_part)
    if toks:
        # 取最后一个 token 作为真实名(混淆前缀 token 通常是 <XX> 转义缀)
        plain = toks[-1]
    if addr == 0 and ndx == 'UND':
        bind = 'UND'
    rows.append((addr, size, typ, bind, ndx, plain, name_part))

rows.sort(key=lambda r: r[0])
with open(OUT, 'w', encoding='utf-8') as f:
    for addr, size, typ, bind, ndx, plain, raw_name in rows:
        f.write(f"{addr:012x} {size:8d} {typ:7s} {bind:6s} {ndx:4s} {plain}\n")

# 输出 SSL/TLS 关键字符号
keys = ('SSL_', 'ssl3_', 'ssl_', 'TLS', 'tls_', 'dtls', 'DTLS', 'EVP_', 'BIO_', 'X509', 'CRYPTO_', 'RAND_', 'ERR_', 'PEM_', 'ENGINE_', 'OPENSSL_', 'BN_', 'RSA', 'AES_', 'HMAC', 'EVP_', 'SHA', 'MD5', 'CONF_', 'ASN1_', 'OBJ_', 'STACK', 'lh_', 'ERR')
hits = [r for r in rows if any(k in r[5] for k in keys)]
print(f"total symbols: {len(rows)}, SSL/crypto-ish: {len(hits)}")
hout = r"C:\Users\20751\Desktop\猫和老鼠\ssl_plain_syms.txt"
with open(hout, 'w', encoding='utf-8') as f:
    for addr, size, typ, bind, ndx, plain, raw_name in hits:
        f.write(f"{addr:012x} {size:8d} {typ:7s} {bind:6s} {ndx:4s} {plain}\n")
print("written", hout)