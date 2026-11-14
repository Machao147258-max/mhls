# -*- coding: utf-8 -*-
# 用已知明文密文对验证 XXTEA 实现/方向/偏移 (对任意 key 检查是否能解出 Lua 头)
import struct, hashlib, os

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac', 'rb').read()
cipher_f = r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin'
cipher = open(cipher_f, 'rb').read()
print('明文:', len(plain), '密文:', len(cipher), '密文头:', cipher[:16].hex())
MASK = 0xffffffff
DELTA = 0x9e3779b9

def decrypt_sub(data, k):
    n = len(data) // 4
    v = list(struct.unpack('<%dI' % n, data))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            mx = ((((z ^ k[ki]) + (z ^ sumv)) & MASK) ^ ((((z >> 3) ^ ((z << 4) & MASK)) + (((z << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[p] = (v[p] - mx) & MASK
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^ (((z ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    return struct.pack('<%dI' % n, *v)

def encrypt_add(data, k):
    n = len(data) // 4
    v = list(struct.unpack('<%dI' % n, data))
    rounds = 6 + 52 // n
    sumv = 0
    for _ in range(rounds):
        sumv = (sumv + DELTA) & MASK
        e = sumv >> 2
        z = v[n - 1]
        for p in range(n - 1):
            y = v[p + 1]
            ki = (p ^ e) & 3
            mx = ((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^ (((z ^ sumv) + (z ^ k[ki])) & MASK)
            v[p] = (v[p] + mx) & MASK
            z = v[p]
        y = v[0]
        ki = ((n - 1) ^ e) & 3
        mx0 = ((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^ (((y ^ sumv) + (y ^ k[ki])) & MASK)
        v[n - 1] = (v[n - 1] + mx0) & MASK
    return struct.pack('<%dI' % n, *v)

# 明文长度 vs 密文: 密文长度-偏移 = 明文+4(长度字)或明文?
print('明文 3574B 检查: 密文', len(cipher), '- 12 =', len(cipher) - 12, '- 16 =', len(cipher) - 16)
# 用 KEY.bin + 所有偏移+方向, 与明文比对
keys = {
    'KEY.bin': bytes.fromhex('53309dfd1b44b11c51df5763e832b73a'),
    'md5udid': hashlib.md5(b'ioscacheudid').digest(),
    '6bb4': bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b'),
}
for kn, key in keys.items():
    k = struct.unpack('<4I', key)
    for off in (12, 16, 8, 0):
        body = cipher[off:]
        pad = (-len(body)) % 4
        body2 = body + b'\x00' * pad
        for mode, fn in [('sub', decrypt_sub), ('add', encrypt_add)]:
            try:
                r = fn(body2, k)
                score = sum(1 for a, b in zip(r[:64], plain[:64]) if a == b)
                flag = ' ★LUA!' if r[:4] == b'\x1bLua' else ''
                if score > 10 or flag:
                    print(f'{kn} off={off} {mode}: 匹配{score}/64 前16={r[:16].hex()}{flag}')
            except Exception:
                pass
print('验证完成')
