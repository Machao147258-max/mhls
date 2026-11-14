# -*- coding: utf-8 -*-
# 变体 XXTEA 解密 (从汇编重构): DELTA=0x61c88647, MX 变体
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()[:3574]
cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
cdata = cipher[12:]

# 汇编重构 (0x8526a8-0x852750 加密循环):
#   v[p] -= MX(z, y, sum, p, e)
#   MX = ((k^y) + (z^sum)) ^ ((z<<2 ^ k>>5) + (z>>3 ^ k<<4))
#   sum += DELTA(0x61c88647)
# 解密 = sum 从 N*DELTA 递减!
DELTA = 0x61c88647
MASK = 0xffffffff

def mx_variant(z, y, s, k):
    t1 = ((k ^ y) + (z ^ s)) & MASK
    t2 = (((z << 2) & MASK) ^ (k >> 5)) + (((z >> 3) & MASK) ^ ((k << 4) & MASK))
    return (t1 ^ (t2 & MASK)) & MASK

def decrypt(data, key, rounds):
    n = len(data) // 4
    v = list(struct.unpack('<%dI' % n, data))
    k = list(struct.unpack('<4I', key))
    sumv = (rounds * DELTA) & MASK
    for _ in range(rounds):
        e = (sumv >> 2) & 3
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            v[p] = (v[p] - mx_variant(z, y, sumv, k[(p & 3) ^ e])) & MASK
            y = v[p]
        z = v[n - 1]
        v[0] = (v[0] - mx_variant(z, y, sumv, k[e])) & MASK
        sumv = (sumv - DELTA) & MASK
    return struct.pack('<%dI' % n, *v)

n = len(cdata) // 4
print(f'n={n}, 密文数据 {len(cdata)}B')
# 密钥 = 密文前 16 字节?
for name, key in {
    'cipher_head': cdata[:16],
    'cipher_tail': cdata[-16:],
    'cipher_12': cdata[12:28],
}.items():
    rounds = 6 + 52 // n
    try:
        dec = decrypt(cdata, key, rounds)
        score = sum(1 for a, b in zip(dec[:64], plain[:64]) if a == b)
        print(f'[{name}]: score {score}/64 dec[:16]={dec[:16].hex()}')
        if score > 20:
            open(r'C:\Users\20751\tomdump\DECRYPTED_VAR.luac', 'wb').write(dec)
    except Exception as ex:
        print(f'[{name}]: {ex}')
print('done')