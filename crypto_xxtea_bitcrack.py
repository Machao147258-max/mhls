# -*- coding: utf-8 -*-
# 位级密钥反推: 从 (C,P) 对反推变体 XXTEA 密钥
# 算法 (精确重构):
#   rounds = 6 + 52//n; sum = rounds * DELTA (DELTA=0x9e3779b9)
#   每轮: e = sum >> 2
#     for p in n-1..1: v[p] -= MX_main(z=v[p-1], k=k[(p^e)&3], sum)
#       MX_main = ((z^k)+(z^sum)) ^ (((z>>3)^(z<<4)) + ((z<<2)^(z>>5)))
#     v[0] -= MX0(z=v[n-1], y=更新后的v[0]?, k=k[e&3], sum)
#       MX0 = (((z>>5)^(y<<2)) + ((z<<4)^(y>>3))) ^ ((z^sum)+(z^k))
#     sum = (sum - DELTA) & 0xffffffff
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()[:3574]
cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
cdata = cipher[12:]
MASK = 0xffffffff

n = len(cdata) // 4
print(f'n = {n}')
v_c = list(struct.unpack('<%dI' % n, cdata))
v_p = list(struct.unpack('<%dI' % (n), plain[:n*4].ljust(n*4, b'\x00')))
# 明文只有 n-1 个字(3574 = 893*4 + 2)最后 2 字节 = padding(可能 0x00 00 或 PKCS!)
print('明文字数:', len(plain)//4, '+', len(plain)%4)

DELTA = 0x9e3779b9
rounds = 6 + 52 // n
sum0 = (rounds * DELTA) & MASK
print(f'rounds={rounds}, sum0={hex(sum0)}')

# 第一轮解密: sum = sum0
# 主循环 p = n-1..1: v[p]_new = v_p[p](明文!)
# MX = (v_c[p] - v_p[p]) & MASK (第一轮!)
# 求 k: MX = ((z^k) + (z^sum)) ^ (C1 + C2), C1 = (z>>3)^(z<<4), C2 = (z<<2)^(z>>5)

def solve_k(mx, z, s):
    """位级求解 k: MX = ((z^k) + (z^s)) ^ ((C1 + C2))
    C1 = (z>>3)^(z<<4), C2 = (z<<2)^(z>>5) (均不含 k!)"""
    C1 = ((z >> 3) ^ ((z << 4) & MASK)) & MASK
    C2 = ((z << 2) & MASK) ^ (z >> 5)
    # 状态: (c_a, c_b, k_bits) 其中 a = (z^k)+B, b = C1+C2
    # B = z^s
    B = (z ^ s) & MASK
    # 逐位 DP (0..31): 位 i:
    #   A_i = z_i ^ k_i; a_i = A_i ^ B_i ^ c_a; c_a' = majority(A_i, B_i, c_a)
    #   b_i = C1_i ^ C2_i ^ c_b; c_b' = majority(C1_i, C2_i, c_b)
    #   要求 MX_i = a_i ^ b_i
    zbits = [(z >> i) & 1 for i in range(32)]
    Bbits = [(B >> i) & 1 for i in range(32)]
    C1b = [(C1 >> i) & 1 for i in range(32)]
    C2b = [(C2 >> i) & 1 for i in range(32)]
    MXb = [(mx >> i) & 1 for i in range(32)]
    # 候选: (k_bits_so_far, c_a, c_b)
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

# 第一轮, 各 p 反推 key 字
e = (sum0 >> 2) & 3
print(f'第一轮 e = {e}')
key_words = {}
for p in range(n - 1, 0, -1):
    z = v_c[p - 1]  # 解密前 v[p-1](密文!)
    mx = (v_c[p] - v_p[p]) & MASK
    ki = (p ^ e) & 3
    k = solve_k(mx, z, sum0)
    if k is None:
        print(f'p={p}: 无解 (z={z:#x} mx={mx:#x})')
        continue
    if ki in key_words and key_words[ki] != k:
        print(f'key[{ki}] 冲突: {key_words[ki]:#x} vs {k:#x} (p={p})')
    else:
        key_words[ki] = k
    if len(key_words) == 4:
        break

print('反推密钥字:', {i: hex(v) for i, v in sorted(key_words.items())})
if len(key_words) >= 4:
    key = struct.pack('<4I', key_words[0], key_words[1], key_words[2], key_words[3])
    print('KEY hex:', key.hex())
    print('KEY repr:', key)
    open(r'C:\Users\20751\tomdump\KEY.bin', 'wb').write(key)
    print('已保存 KEY.bin!')
else:
    print('未完整反推(需更多样本)')