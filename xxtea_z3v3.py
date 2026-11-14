# -*- coding: utf-8 -*-
# Z3 全链求解 v3: 确认模型(与 0x8526a8 反汇编逐指令一致) + 约束前 N 字
# 解密: rounds=6+52//n, sum 从 rounds*DELTA 递减, y 链式更新, k[(p^e)&3]
import struct, sys
from z3 import *

PLAIN = r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac'
CIPHER = r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin'
MASK32 = 0xffffffff
DELTA = 0x9e3779b9

plain = open(PLAIN, 'rb').read()
cipher = open(CIPHER, 'rb').read()
cdata = cipher[12:]
n = len(cdata) // 4
rounds = 6 + 52 // n
v_c = list(struct.unpack('<%dI' % n, cdata))
v_p_full = plain[:n*4] + b'\x00' * (n*4 - len(plain))
v_p = list(struct.unpack('<%dI' % n, v_p_full))
print(f'n={n} rounds={rounds} sum0={hex((rounds*DELTA)&MASK32)}', flush=True)

K = int(sys.argv[1]) if len(sys.argv) > 1 else 32
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

# 解密模型 (与反汇编一致)
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
s.set(timeout=1000000)  # 1000s
# 前 K 字全约束 (K=32 含 luac 头 12B + source)
for i in range(K):
    s.add(v[i] == v_p[i])
print(f'约束 {K} 字...', flush=True)
res = s.check()
print('结果:', res, flush=True)
if res == sat:
    m = s.model()
    key = bytes()
    for i in range(4):
        key += struct.pack('<I', m.eval(k[i]).as_long() & 0xffffffff)
    print('KEY:', key.hex(), flush=True)
    open(r'C:\Users\20751\tomdump\KEY2.bin', 'wb').write(key)
    print('已存 KEY2.bin', flush=True)
