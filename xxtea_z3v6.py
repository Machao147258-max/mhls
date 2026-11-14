# -*- coding: utf-8 -*-
# z3v6 诊断: 单字约束测模型速度与明文假设
# 结论判定: 1字 SAT(快) → 模型OK; UNSAT(快) → 明文假设错; 超时 → 实例本身难
import struct, sys, time
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

def solve(known_map, tag, timeout=30000):
    k = [BitVec(f'k{i}', 32) for i in range(4)]
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
    s.set(timeout=timeout)
    for i, val in known_map.items():
        s.add(v[i] == val)
    t0 = time.time()
    res = s.check()
    dt = time.time() - t0
    print(f'{tag}: {res} ({dt:.1f}s)', flush=True)
    if res == sat:
        m = s.model()
        key = b''.join(struct.pack('<I', m.eval(k[i]).as_long() & 0xffffffff) for i in range(4))
        print(f'  key={key.hex()}', flush=True)
        return key
    return None

# 诊断 1: word 24 == 0 (最后字零)
solve({24: 0}, '诊断1: w24=0')
# 诊断 2: word 0 == '{\n    ' (JSON 开头)
solve({0: 0x20200a7b}, '诊断2: w0=JSON头')
# 诊断 3: word 1 == '"ver'
solve({1: 0x72657622}, '诊断3: w1="ver')
# 诊断 4: word 0-3 == '{\n    "version": '
solve({0: 0x20200a7b, 1: 0x72657622, 2: 0x6e6f6973, 3: 0x20203a22}, '诊断4: w0-3=JSON前缀')
