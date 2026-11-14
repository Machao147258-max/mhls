# -*- coding: utf-8 -*-
"""libepay-crypto.so 深度侦查: ELF 元数据 + 字符串特征(AES/RSA/哈希/xxtea/私钥) + 导出"""
import re, struct, os

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()
print("size = %d (0x%x)" % (len(d), len(d)))

# ELF 头
e = struct.unpack_from('<16sHHIQQQIHHHHHH', d, 0)
print("magic=%s class=%d machine=0x%x" % (e[0], e[1], e[3]))
assert d[:4] == b'\x7fELF'

# 找节头 (.rodata/.text 范围近似)
# strings 扫描 (可打印串 >= 5)
strs = re.findall(rb'[\x20-\x7e]{5,}', d)
joined = b'\n'.join(strs)

pats = {
 'AES': [b'\bAES', b'AES-', b'aes', b'CBC', b'ECB', b'GCM', b'SecretKeySpec', b'IvParameterSpec'],
 'RSA': [b'RSA', b'rsa', b'PrivateKey', b'PublicKey', b'PEM', b'PKCS'],
 'hash': [b'MD5', b'SHA', b'md5', b'sha', b'HMAC', b'xxhash', b'crc32'],
 'xxtea': [b'xxtea', b'XXTEA', b'XTEA', b'TEA'],
 'key': [b'key', b'secret', b'iv', b'nonce', b'padding', b'salt'],
 'ecc': [b'EC_', b'curve', b'P-256', b'secp', b'ed25519'],
 'base64': [b'base64', b'BASE64'],
}
for name, plist in pats.items():
    hits = set()
    for p in plist:
        for m in re.finditer(re.escape(p), joined):
            s = strs[m.start() // (len(joined)//max(1,len(strs)))] if False else None
            break
    # 更简单: 直接统计
    cnt = sum(joined.count(p) for p in plist)
    print("[%s] 命中总数 %d" % (name, cnt))

# JNI 方法/签名
print("\n== JNI 相关串 ==")
jni = [s.decode('latin1') for s in strs if b'netease' in s.lower() or b'com/' in s or b'Ljavax' in s or b'Lcom' in s]
for s in jni[:60]:
    print("  ", s)

# 硬编码密钥特征: 32/16 字节 hex 串
print("\n== 疑似硬编码 hex 种子 (16/32字节16进制) ==")
hexc = re.findall(rb'(?<![0-9a-fA-F])([0-9a-fA-F]{32}|[0-9a-fA-F]{64})(?![0-9a-fA-F])', d)
for h in hexc[:20]:
    print("  ", h.decode())

# 导出符号
print("\n== 导出符号 ==")
try:
    exp = re.findall(rb'getFlexibleSecret|getAesKey|base64|CryptoFactor|Java_', joined)
    for e in sorted(set(exp))[:40]:
        print("  ", e.decode())
except Exception as ex:
    print("  err", ex)