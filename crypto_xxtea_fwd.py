# -*- coding: utf-8 -*-
# 正确反推: 加密第 1 轮 (sum=0!) 只依赖明文 → 解 k
# 加密: v[p] += MX(z=v[n-1], y=v[p], k[(p^e)&3], sum)
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()[:3574]
cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
cdata = cipher[12:]
MASK = 0xffffffff
n = len(cdata) // 4
v_p = list(struct.unpack('<%dI' % n, plain[:n*4].ljust(n*4, b'\x00')))
DELTA = 0x9e3779b9
# 加密第 1 轮 sum = 0 (e = 0)
sum0 = 0
e = 0
z_fixed = v_p[n - 1]
print(f'n={n} z_fixed={z_fixed:#x}')

def solve_k(mx, z, y, s):
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

# 加密第 1 轮: p = 1..n-1? 或 p = 0..n-2? (汇编 0x8528a8: add w3, w4, #1; 0x8528c4: cmp w0, w3)
# 处理 v[p+1]? 我们不知道确切的 p 范围/顺序 — 试两种!
# MX 公式 (加密 0x8528d0-0x8528e8): ((z^k)+(y^sum)) ^ ((z<<4^y>>3)+(z>>5^y<<2))
# v[p]_new = v[p]_old + MX; 但我们需要 v[p]_new(中间态)来列方程?
# 不对!! 方程 = v[p]_new = v[p] + MX → MX = v[p]_new - v[p] — v[p]_new 未知!
# 但!!! 加密第 1 轮后 = 中间态(未知!)— 无法列方程!!
# 所以加密第 1 轮无法反推(中间态未知)!
print('加密第 1 轮无法反推(中间态未知!)')
print('改用: 解密最后一轮 (sum = DELTA, 输出 = 明文) — 但输入未知!')
print('唯一可行: 全链求解(6 轮联立!) — 每字每轮 1 方程(未知 = 中间态 + k)')
print('简化: 用 n=2 的特殊对? 或 2 块的小文件!')