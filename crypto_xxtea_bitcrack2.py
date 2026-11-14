# -*- coding: utf-8 -*-
# 修正位级密钥反推: 主循环 MX = ((z^k)+(y^sum)) ^ (((y>>3)^(z<<4)) + ((y<<2)^(z>>5)))
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()[:3574]
cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
cdata = cipher[12:]
MASK = 0xffffffff
n = len(cdata) // 4
v_c = list(struct.unpack('<%dI' % n, cdata))
v_p = list(struct.unpack('<%dI' % n, plain[:n*4].ljust(n*4, b'\x00')))

DELTA = 0x9e3779b9
rounds = 6 + 52 // n
sum0 = (rounds * DELTA) & MASK
print(f'n={n} rounds={rounds} sum0={hex(sum0)} e0={(sum0>>2)&3}')

def solve_k(mx, z, y, s):
    """MX = ((z^k) + (y^s)) ^ (C1 + C2); C1 = (y>>3)^(z<<4), C2 = (y<<2)^(z>>5)"""
    C1 = ((y >> 3) ^ ((z << 4) & MASK)) & MASK
    C2 = ((y << 2) & MASK) ^ (z >> 5)
    B = (y ^ s) & MASK
    zbits = [(z >> i) & 1 for i in range(32)]
    Bbits = [(B >> i) & 1 for i in range(32)]
    C1b = [(C1 >> i) & 1 for i in range(32)]
    C2b = [(C2 >> i) & 1 for i in range(32)]
    MXb = [(mx >> i) & 1 for i in range(32)]
    cands = [(0, 0, 0)]
    for i in range(32):
        new = []
        for kb, ca, cb in cands:
            for ki in (0, 1):
                A = zbits[i] ^ ki
                ai = A ^ Bbits[i] ^ ca
                ca2 = ((A & Bbits[i]) | (A & ca) | (Bbits[i] & ca))
                bi = C1b[i] ^ C2b[i] ^ cb
                cb2 = ((C1b[i] & C2b[i]) | (C1b[i] & cb) | (C2b[i] & cb))
                if (ai ^ bi) == MXb[i]:
                    new.append((kb | (ki << i), ca2, cb2))
        cands = new
        if not cands:
            return None
    return cands[0][0]

# 第一轮解密 (sum = sum0):
#   y 初始 = v_c[0](密文!); p = n-1..1: MX 用 y = 上一个更新的字(初始 v_c[0]!)
#   输出 v_p[p](明文!)
e = (sum0 >> 2) & 3
key_words = {}
y = v_c[0]
for p in range(n - 1, 0, -1):
    z = v_c[p - 1]
    mx = (v_c[p] - v_p[p]) & MASK
    ki = (p ^ e) & 3
    k = solve_k(mx, z, y, sum0)
    if k is None:
        print(f'p={p}: 无解')
        break
    if ki in key_words and key_words[ki] != k:
        print(f'key[{ki}] 冲突 @p={p}: {key_words[ki]:#x} vs {k:#x}')
    key_words[ki] = k
    y = v_p[p]  # 下一轮 y = 更新后的 v[p]
    if len(key_words) == 4:
        print(f'4 个字在 p={p} 集齐')
        break

print('反推密钥字:', {i: hex(v) for i, v in sorted(key_words.items())})
if len(key_words) == 4:
    key = struct.pack('<4I', key_words[0], key_words[1], key_words[2], key_words[3])
    print('KEY:', key.hex())
    open(r'C:\Users\20751\tomdump\KEY.bin', 'wb').write(key)
    print('已保存!')