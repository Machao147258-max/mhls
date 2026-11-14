# -*- coding: utf-8 -*-
# 从 live_segs 提取候选 key(过滤类名) → 黄金对验证
import re, struct, os, glob

MASK32 = 0xffffffff
DELTA = 0x9e3779b9
PLAIN = r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac'
CIPHER = r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin'

plain = open(PLAIN, 'rb').read()
cipher = open(CIPHER, 'rb').read()
cdata = cipher[12:]
n = len(cdata) // 4
v_c = list(struct.unpack('<%dI' % n, cdata))
ref = (plain[:n*4] + b'\x00' * n*4)[:n*4]

def decrypt(data, key):
    v = list(struct.unpack('<%dI' % n, data))
    k = list(struct.unpack('<4I', key.ljust(16, b'\x00')[:16]))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK32
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

def score(body):
    return sum(1 for a, b in zip(body[:128], ref[:128]) if a == b)

BAD = re.compile(rb'[/\\()\[\];$,<>:=\{\}@#]')
GOOD = re.compile(rb'^[A-Za-z0-9_.\-]{16}$')
cands = set()
for fn in glob.glob(r'C:\Users\20751\tomdump\live_segs\*.bin'):
    b = open(fn, 'rb').read()
    for m in re.finditer(rb'[\x20-\x7e]{16}', b):
        s = m.group(0)[:16]
        if not GOOD.match(s): continue
        if s[:4].lower() in (b'com/', b'org/', b'java', b'andr', b'kotl', b'io.'): continue
        cands.add(s)
print(f'候选 {len(cands)}', flush=True)
best = []
for c in cands:
    sc = score(decrypt(cdata, c))
    if sc > 64:
        best.append((sc, c))
best.sort(reverse=True)
print('=== >64/128 命中 ===', flush=True)
for sc, c in best[:30]:
    print(f'{sc} {c!r}', flush=True)
if not best:
    print('无命中', flush=True)
