# -*- coding: utf-8 -*-
# 修正反推: p 的 y = v_p[p+1] (p=n-1 时 y = v_c[0])
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
e = (sum0 >> 2) & 3
print(f'n={n} rounds={rounds} sum0={hex(sum0)} e={e}')

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

kw = {}
fails = 0
for p in range(n - 1, 0, -1):
    z = v_c[p - 1]
    y = v_c[0] if p == n - 1 else v_p[p + 1]
    mx = (v_c[p] - v_p[p]) & MASK
    ki = (p ^ e) & 3
    k = solve_k(mx, z, y, sum0)
    if k is None:
        fails += 1
        if fails <= 3:
            print(f'p={p}: 无解 (ki={ki})')
        continue
    if ki in kw and kw[ki] != k:
        print(f'key[{ki}] 冲突 @p={p}: {kw[ki]:#x} vs {k:#x}!!')
    else:
        kw[ki] = k
    if len(kw) == 4:
        print(f'4 字集齐 @p={p}')
        break
print(f'无解数: {fails}')
print('密钥字:', {i: hex(v) for i, v in sorted(kw.items())})
if len(kw) == 4:
    key = struct.pack('<4I', kw[0], kw[1], kw[2], kw[3])
    print('KEY:', key.hex())
    print('KEY repr:', key)
    open(r'C:\Users\20751\tomdump\KEY.bin', 'wb').write(key)
    print('已保存!')