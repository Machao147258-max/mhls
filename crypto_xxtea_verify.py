# -*- coding: utf-8 -*-
# 完整解密验证 (用反推的密钥!)
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()[:3574]
cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
cdata = cipher[12:]
MASK = 0xffffffff
n = len(cdata) // 4
DELTA = 0x9e3779b9

key = open(r'C:\Users\20751\tomdump\KEY.bin','rb').read()
k = list(struct.unpack('<4I', key))
print('KEY:', key.hex(), k)

def decrypt(data):
    v = list(struct.unpack('<%dI' % n, data))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        # 主循环 p = n-1..1
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            # MX = ((z^k)+(z^sum)) ^ (((z>>3)^(z<<4)) + ((z<<2)^(z>>5)))
            mx = ((((z ^ k[ki]) + (z ^ sumv)) & MASK) ^
                  ((((z >> 3) ^ ((z << 4) & MASK)) + (((z << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[p] = (v[p] - mx) & MASK
            y = v[p]
        # v[0]
        z = v[n - 1]
        ki = e & 3
        # MX0 = (((z>>5)^(y<<2)) + ((z<<4)^(y>>3))) ^ ((z^sum)+(z^k))
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^
               (((z ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    return struct.pack('<%dI' % n, *v)

dec = decrypt(cdata)
print('解密前 32B:', dec[:32].hex())
print('明文   32B:', plain[:32].hex())
score = sum(1 for a, b in zip(dec[:128], plain[:128]) if a == b)
print(f'前 128B 匹配: {score}/128')
if dec.startswith(b'\x1bLuaQ'):
    print('🎉🎉🎉 解密成功!! 是合法 luac!')
    open(r'C:\Users\20751\tomdump\DECRYPTED_FINAL.luac','wb').write(dec)
    print('已保存 DECRYPTED_FINAL.luac')
elif score > 100:
    print('高度匹配(检查 padding!)')
else:
    print('不匹配(算法还有细节差异!)')
    # 试试主循环也用它自己的 MX0 形式(对称!)
    def decrypt2(data):
        v = list(struct.unpack('<%dI' % n, data))
        rounds = 6 + 52 // n
        sumv = (rounds * DELTA) & MASK
        while sumv != 0:
            e = sumv >> 2
            for p in range(n - 1, 0, -1):
                z = v[p - 1]
                ki = (p ^ e) & 3
                mx = ((((z >> 5) ^ ((z << 2) & MASK)) + (((z << 4) & MASK) ^ (z >> 3))) & MASK) ^ \
                     (((z ^ sumv) + (z ^ k[ki])) & MASK) & MASK
                v[p] = (v[p] - mx) & MASK
            z = v[n - 1]
            ki = e & 3
            mx0 = ((((z >> 5) ^ ((z << 2) & MASK)) + (((z << 4) & MASK) ^ (z >> 3))) & MASK) ^ \
                  (((z ^ sumv) + (z ^ k[ki])) & MASK) & MASK
            v[0] = (v[0] - mx0) & MASK
            sumv = (sumv - DELTA) & MASK
        return struct.pack('<%dI' % n, *v)
    dec2 = decrypt2(cdata)
    score2 = sum(1 for a, b in zip(dec2[:128], plain[:128]) if a == b)
    print(f'变体2 前 128B 匹配: {score2}/128  dec2[:16]={dec2[:16].hex()}')