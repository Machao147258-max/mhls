# -*- coding: utf-8 -*-
# z3v5 块1: version.bin (n=25, rounds=8) — 零填充尾部字约束
# 常数折叠: e 值直接算好; key 纯 128-bit
import struct, sys
from z3 import *

CIPHER = r'C:\Users\20751\tomdump\cdn_pull\package\src\f7415dd468c3de817383d2e30c34071f.bin'
cipher = open(CIPHER, 'rb').read()
cdata = cipher[12:]
n = len(cdata) // 4
rounds = 6 + 52 // n
v_c = list(struct.unpack('<%dI' % n, cdata))
MASK32 = 0xffffffff
DELTA = 0x9e3779b9
sum0 = (rounds * DELTA) & MASK32
es = [((sum0 - r * DELTA) & MASK32) >> 2 & 3 for r in range(rounds)]
print(f'n={n} rounds={rounds} sum0=0x{sum0:08x} e序列={es}', flush=True)

def build(known_map, k, tag):
    def pick(ki):
        return If(ki == 0, k[0], If(ki == 1, k[1], If(ki == 2, k[2], k[3])))
    def MX(z, y, sumv, ki):
        t1 = (z ^ pick(ki)) + (y ^ sumv)
        t2 = ((y >> 3) ^ LShR(z << 4, 0)) + ((y << 2) ^ LShR(z, 5))
        return (t1 ^ t2) & 0xffffffff
    def MX0(z, y, sumv, ki):
        t1 = (LShR(z, 5) ^ (y << 2)) + ((z << 4) ^ LShR(y, 3))
        t2 = (y ^ sumv) + (z ^ pick(ki))
        return (t1 ^ t2) & 0xffffffff
    v = [BitVecVal(x, 32) for x in v_c]
    sumv = sum0
    for r in range(rounds):
        e = es[r]
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            v[p] = (v[p] - MX(z, y, sumv, ki)) & 0xffffffff
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        v[0] = (v[0] - MX0(z, y, sumv, ki)) & 0xffffffff
        sumv = (sumv - DELTA) & MASK32
    s = Solver()
    s.set(timeout=60000)
    for i, val in known_map.items():
        s.add(v[i] == val)
    res = s.check()
    if res == sat:
        m = s.model()
        key = b''.join(struct.pack('<I', m.eval(k[i]).as_long() & 0xffffffff) for i in range(4))
        print(f'★ {tag}: SAT key={key.hex()}', flush=True)
        return key
    print(f'{tag}: {res}', flush=True)
    return None

# 明文 JSON 长度假设 L: 零字 = words ceil(L/4)..n-1
for L in (44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 56, 60, 64):
    zstart = (L + 3) // 4
    km = {i: 0 for i in range(zstart, n)}
    if len(km) < 4: continue
    k = [BitVec(f'k{i}', 32) for i in range(4)]
    key = build(km, k, f'L={L} 零字 {zstart}-{n-1} ({len(km)}字)')
    if key:
        sys.exit(0)
print('块1完成: 无解', flush=True)
