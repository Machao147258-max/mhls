#!/usr/bin/env python3
# XXTEA 解密器 + key 字典爆破 — 本地加密数据
import struct

DELTA = 0x9E3779B9

def xxtea_decrypt(data: bytes, key: bytes) -> bytes:
    """标准 XXTEA 解密 (Little-Endian, 与 xxtea_disasm 对齐)"""
    n = len(data) // 4
    if n < 2:
        return b''
    v = list(struct.unpack('<%dI' % n, data[:n * 4]))
    k = list(struct.unpack('<4I', key[:16].ljust(16, b'\x00')))
    q = 6 + 52 // n
    s = (q * DELTA) & 0xFFFFFFFF
    while s:
        e = (s >> 2) & 3
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - (((z >> 5 ^ v[(p + 1) % n] << 2) + (v[(p + 1) % n] >> 3 ^ z << 4)) ^ ((s ^ v[(p + 1) % n]) + (k[(p & 3) ^ e] ^ z)))) & 0xFFFFFFFF
        z = v[n - 1]
        v[0] = (v[0] - (((z >> 5 ^ v[1] << 2) + (v[1] >> 3 ^ z << 4)) ^ ((s ^ v[1]) + (k[0 ^ e] ^ z)))) & 0xFFFFFFFF
        s = (s - DELTA) & 0xFFFFFFFF
    return struct.pack('<%dI' % n, *v)

# 候选 key (16 字节)
keys = [
    b'netease', b'tom', b'h18', b'cocos', b'netease.com', b'netEaseTom',
    b'netease_tom', b'TomH18', b'7.45.0', b'h18tom', b'tom163', b'netease163',
    b'cocos2dlua', b'cocos2d-x', b'xindagag', b'248850489', b'be1c235ad80959f7',
    b'debcbe7ca672d9d876', b'8e066e23b43ea4e3', b'netease.p1', b'netease_p1',
    b'nc_tom', b'tomh18', b'muMu123', b'Qwerty123', b'1234567890abcdef',
    b'abcdefghijklmnop', b'h18h18h18h18h18', b'1234567890123456',
]

# 目标数据
targets = {
    'LAUNCH_UDID': bytes.fromhex('75e6dc6deedc6baef677d77cef'),
    'AVATAR_MD5_1': bytes.fromhex('69de387356fcebc7fad7b69b7b6e9dedde9fdbd75cdb5e1f'),
    'AVATAR_MD5_2': bytes.fromhex('6f96f87b5d76f38f34dfc6bcdbdd397347f8eb7d5e7deef4'),
    'firstOpenTime': bytes.fromhex('d7bf3af34d7ddb'),
}

# 尝试: 原长度 + 补齐到 8 倍数
def try_pads(data):
    pads = []
    L = len(data)
    for plen in [L, (L + 7) // 8 * 8, L + 1]:
        if plen >= 8:
            pads.append(data.ljust(plen, b'\x00'))
    return pads

for name, ct in targets.items():
    print(f'=== {name} (len={len(ct)}) ===')
    for pad in try_pads(ct):
        for k in keys:
            try:
                pt = xxtea_decrypt(pad, k)
                printable = sum(1 for c in pt if 32 <= c < 127 or c == 0) / max(len(pt), 1)
                if printable > 0.7 and len(pt) >= 8:
                    print(f'  key={k!r} pad={len(pad)} -> {pt!r}')
            except Exception:
                pass
print('done')