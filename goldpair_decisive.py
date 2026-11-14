# -*- coding: utf-8 -*-
# 决定性验证 v2: 标准 XXTEA 解密(与反汇编一致) × 候选 key × 偏移
import struct, re, sys

PLAIN = r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac'
CIPHER = r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin'
MASK32 = 0xffffffff
DELTA = 0x9e3779b9

def log(*a):
    print(*a, flush=True)

plain = open(PLAIN, 'rb').read()
cipher = open(CIPHER, 'rb').read()
log(f'plain={len(plain)}B cipher={len(cipher)}B')

def decrypt(data, key):
    n = len(data) // 4
    if n < 2: return None
    v = list(struct.unpack('<%dI' % n, data))
    k = list(struct.unpack('<4I', key.ljust(16, b'\x00')[:16]))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK32
    if sumv == 0: return None
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            mx = ((((z ^ k[ki]) + (y ^ sumv)) & MASK32) ^
                  ((((y >> 3) ^ ((z << 4) & MASK32)) + (((y << 2) & MASK32) ^ (z >> 5))) & MASK32)) & MASK32
            v[p] = (v[p] - mx) & MASK32
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK32)) + (((z << 4) & MASK32) ^ (y >> 3))) & MASK32) ^
               (((y ^ sumv) + (z ^ k[ki])) & MASK32)) & MASK32
        v[0] = (v[0] - mx0) & MASK32
        sumv = (sumv - DELTA) & MASK32
    return struct.pack('<%dI' % n, *v)

def score(body, ref, check_len=256):
    return sum(1 for a, b in zip(body[:check_len], ref[:check_len]) if a == b)

cands = {}
cands['8ar/aaa/pckaere8'] = b'8ar/aaa/pckaere8'
cands['KEY.bin'] = open(r'C:\Users\20751\tomdump\KEY.bin', 'rb').read()
cands['xxtea_default'] = bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b')
cands['epaa5ec7'] = b'epaa5ec7' + b'\x00' * 8
cands['epaa5ec7x2'] = b'epaa5ec7' * 2
try:
    for i, line in enumerate(open(r'C:\Users\20751\tomdump\extra_keys.txt', 'rb').read().split()):
        if len(line) == 32:  # 16 字节 hex
            cands[f'extra_{i}'] = bytes.fromhex(line.decode())
except FileNotFoundError:
    pass
log(f'候选 key 数: {len(cands)}')

best = []
for off in (8, 12):
    cdata = cipher[off:]
    n = len(cdata) // 4
    cdata = cdata[:n*4]
    ref = (plain[:n*4] + b'\x00' * n*4)[:n*4]
    for name, key in cands.items():
        body = decrypt(cdata, key)
        if body is None: continue
        sc = score(body, ref)
        if sc > 100:
            best.append((sc, off, name, key.hex()))
best.sort(reverse=True)
log('=== 匹配 >100/256 的候选 ===')
for sc, off, name, kh in best[:30]:
    log(f'score={sc:3d} off={off} key={name} = {kh}')
if not best:
    log('无候选命中 — key 不在候选集里')
