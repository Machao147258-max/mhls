# -*- coding: utf-8 -*-
# 小文件已知明文攻击: version.bin (n=25, rounds=8)
# 明文 = version.json 格式 + 零填充; 枚举 (version, hotfixVersion) 候选
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
print(f'n={n} rounds={rounds} payload={len(cdata)}B', flush=True)

def solve(p_known_map, tag):
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
    sumv = BitVecVal((rounds * DELTA) & MASK32, 32)
    for r in range(rounds):
        e = LShR(sumv, 2)
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            v[p] = (v[p] - MX(z, y, sumv, ki)) & 0xffffffff
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        v[0] = (v[0] - MX0(z, y, sumv, ki)) & 0xffffffff
        sumv = (sumv - BitVecVal(DELTA, 32)) & 0xffffffff
    s = Solver()
    s.set(timeout=60000)
    for i, val in p_known_map.items():
        s.add(v[i] == val)
    res = s.check()
    if res == sat:
        m = s.model()
        key = b''.join(struct.pack('<I', m.eval(k[i]).as_long() & 0xffffffff) for i in range(4))
        print(f'★ {tag}: SAT key={key.hex()}', flush=True)
        open(r'C:\Users\20751\tomdump\KEY3.bin', 'wb').write(key)
        return key
    print(f'{tag}: {res}', flush=True)
    return None

# 候选明文格式: 两种 JSON 风格 × V/H 组合
templates = [
    ('{{spaces}}', '{{\n    "version": {V}, \n    "hotfixVersion": {H}\n}}'),
    ('compact', '{{"version":{V},"hotfixVersion":{H}}}'),
]
V_cands = ['7', '49', '492', '7492', '7.49.2', '7450', '-1', '0', '7492.0']
H_cands = ['300', '435', '492', '0', '1', '7', '45', '30000']

total = 0
for tname, tpl in templates:
    for V in V_cands:
        for H in H_cands:
            p = tpl.format(V=V, H=H).encode()
            if len(p) > n * 4: continue
            full = p + b'\x00' * (n * 4 - len(p))
            known = {}
            for i in range(n):
                seg = full[i*4:(i+1)*4]
                if seg == b'\x00\x00\x00\x00':
                    known[i] = 0  # 零字已知
                else:
                    # 全可打印/已知结构字
                    known[i] = struct.unpack('<I', seg)[0]
            total += 1
            key = solve(known, f'{tname} V={V} H={H}')
            if key:
                print('KEY FOUND:', key.hex(), flush=True)
                sys.exit(0)
print(f'完成, 尝试 {total} 组合, 无解')
