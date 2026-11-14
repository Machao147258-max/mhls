# -*- coding: utf-8 -*-
# debug: 反推 key 后, 第一轮输出 vs 明文 (逐字!)
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()[:3574]
cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
cdata = cipher[12:]
MASK = 0xffffffff
n = len(cdata) // 4
DELTA = 0x9e3779b9
key = open(r'C:\Users\20751\tomdump\KEY.bin','rb').read()
k = list(struct.unpack('<4I', key))
print('KEY:', key.hex())

rounds = 6 + 52 // n
sum0 = (rounds * DELTA) & MASK
v = list(struct.unpack('<%dI' % n, cdata))
e = sum0 >> 2
y = v[0]
# 第一轮 (sum = sum0)
for p in range(n - 1, 0, -1):
    z = v[p - 1]
    ki = (p ^ e) & 3
    mx = ((((z ^ k[ki]) + (y ^ sum0)) & MASK) ^
          ((((y >> 3) ^ ((z << 4) & MASK)) + (((y << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
    v[p] = (v[p] - mx) & MASK
    y = v[p]
z = v[n - 1]
ki = e & 3
mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^
       (((y ^ sum0) + (z ^ k[ki])) & MASK)) & MASK
v[0] = (v[0] - mx0) & MASK

# 对比明文 (字级!)
vp = list(struct.unpack('<%dI' % n, plain[:n*4].ljust(n*4, b'\x00')))
match = sum(1 for a, b in zip(v, vp) if a == b)
print(f'第一轮输出 vs 明文: {match}/{n} 字匹配')
# 前 8 字
for i in range(8):
    print(f'  [{i}] dec={v[i]:08x} plain={vp[i]:08x} {"✓" if v[i]==vp[i] else "✗"}')
# 明文头部字节 vs 第一轮输出字节
decb = struct.pack('<%dI' % n, *v)
print('dec  :', decb[:32].hex())
print('plain:', plain[:32].hex())