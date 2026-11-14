# -*- coding: utf-8 -*-
"""libepay-crypto.so: 1) 解密 0xd10f0 处 26B XOR 硬编码密钥材料  2) 确认注册表 fnPtr"""
import struct
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()

# --- 1) 密钥材料解密 ---
buf_off = 0xd10f0      # x20 = 0xd1000+0xf0
key16 = d[0xa9900:0xa9900+16]   # 0x44f68 ldr q0, [x8,#0x900]  x8=0xa9000
print("NEON XOR key(16B): %s" % key16.hex())
enc = bytearray(d[buf_off:buf_off+0x1a])
print("密文 (26B):        %s" % enc.hex())

# 前 16 字节 XOR key16
plain = bytearray(26)
for i in range(16):
    plain[i] = enc[i] ^ key16[i]
# 后 10 字节 keys (按反汇编对齐)
keys = {0x10:0xa3, 0x11:0x5b, 0x12:0x8f, 0x13:0x05, 0x14:0xc9,
        0x15:0x8b, 0x16:0x7d, 0x17:0xcb, 0x18:0xa3, 0x19:0x5b}
for off, k in keys.items():
    plain[off] = enc[off] ^ k
print("明文 (26B):        %s" % plain.hex())
print("明文 ascii:        %r" % bytes(plain))

# --- 2) 注册表确认 (0x45008~0x452c0 构建的条目) ---
print("\n== JNI 注册条目 (name VA, sig VA, fnPtr, name字符串) ==")
entries = [
 (0xa9bcc, 0xadb8, 0x4a3f4, 'getFlexibleSecret'),
 (0xa9bde, 0xadf, 0x4a60c, '?0xbde'),
 (0xa9bea, 0xadf6, 0x4a6fc, 'getAesKey'),
 (0xa9bf4, 0xadb8, 0x4a7ec, '?0xbf4'),
 (0xa9bfb, 0xae37, 0x4a8e4, '?0xbfb'),
 (0xa9c05, 0xae8a, 0x4a9dc, '?0xc05'),
 (0xa9c0c, 0xaeb3, 0x4aad4, '?0xc0c'),
 (0xa9c13, 0xaedc, 0x4abc4, 'base64Encode'),
 (0xa9c20, 0xaedc, 0x4acb4, 'base64Decode'),
 (0xa9c2d, 0xae37, 0x4adac, '?0xc2d'),
]
for name_va, sig_va, fn, guess in entries:
    name_s = d[name_va:].split(b'\x00')[0].decode('latin1','replace')
    sig = d[sig_va:].split(b'\x00')[0].decode('latin1','replace') if 0 < sig_va < len(d) else '?'
    print("  name=%-24s sig=%-30s fnPtr=%#x  (%s)" % (name_s, sig, fn, guess))