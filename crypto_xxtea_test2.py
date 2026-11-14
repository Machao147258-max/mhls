# -*- coding: utf-8 -*-
# XXTEA 测试: common_utils (3574B 明文) ↔ 63e9d1d1.bin (3580B 密文)
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()
plain = plain[:3574]
print('明文头:', plain[:32].hex())

cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
print('密文:', len(cipher), '头:', cipher[:16].hex())
# 剥 X1V5fzTo + 4 字节
assert cipher.startswith(b'X1V5fzTo'), '格式不对'
cdata = cipher[12:]
print('密文数据:', len(cdata))

def xxtea_decrypt(data, key):
    n = len(data) // 4
    if n < 2: return None
    v = list(struct.unpack('<%dI' % n, data))
    k = list(struct.unpack('<4I', key))
    DELTA = 0x9e3779b9
    MASK = 0xffffffff
    def MX(z, y, sum, p, e):
        return ((((z >> 5) ^ (y << 2)) + ((y >> 3) ^ (z << 4))) ^ ((sum ^ y) + (k[(p & 3) ^ e] ^ z))) & MASK
    rounds = 6 + 52 // n
    if n == 2:
        z, y = v[0], v[1]
        sums = (rounds * DELTA) & MASK
        for _ in range(rounds):
            y = (y - ((((z << 4) ^ (z >> 5)) + z) ^ (sums + k[(sums >> 11) & 3]))) & MASK
            sums = (sums - DELTA) & MASK
            z = (z - ((((y << 4) ^ (y >> 5)) + y) ^ (sums + k[sums & 3]))) & MASK
        v[0], v[1] = z, y
    else:
        y = v[0]
        sums = (rounds * DELTA) & MASK
        while sums != 0:
            e = (sums >> 2) & 3
            p = n - 1
            while p > 0:
                z = v[p - 1]
                v[p] = (v[p] - MX(z, y, sums, p, e)) & MASK
                y = v[p]
                p -= 1
            z = v[n - 1]
            v[0] = (v[0] - MX(z, y, sums, 0, e)) & MASK
            y = v[0]
            sums = (sums - DELTA) & MASK
    return struct.pack('<%dI' % n, *v)

cands = {
    'mem_consts': bytes.fromhex('b979379e157c4a7fb979379e09c9bcf3'),
    'mem_d0':     bytes.fromhex('7376867a164fcaeeb979379e18000000'),
    'mem_d1':     bytes.fromhex('157c4a7fb979379e0000000000000000'),
    'mem_sha':    bytes.fromhex('6a09e667bb67ae853c6ef372f3bcc909'),
    'old_key':    b'8ar/aaa/pckaere8',
    'old_sec':    b'epaa5ec7',
    'zero':       b'\x00'*16,
    'netease':    b'neteasegamesh18',
}
for name, key in cands.items():
    key = key[:16].ljust(16, b'\x00')
    try:
        dec = xxtea_decrypt(cdata, key)
        # 比对明文头!
        match = dec[:16] == plain[:16]
        score = sum(1 for a, b in zip(dec[:64], plain[:64]) if a == b)
        print(f'{name}: {"✓✓✓ 命中!!" if match else "✗"} 头匹配 {score}/64  dec[:16]={dec[:16].hex()}')
        if match:
            open(r'C:\Users\20751\tomdump\DECRYPTED_OK.luac', 'wb').write(dec)
    except Exception as ex:
        print(f'{name}: {ex}')