# -*- coding: utf-8 -*-
# 候选 key 双向 XXTEA 解密测试
import struct, os

data = open(r'C:\Users\20751\tomdump\test_cipher.bin', 'rb').read()
body = data[16:]
DELTA = 0x9E3779B9
MASK = 0xFFFFFFFF

def to_words(b):
    return list(struct.unpack('<%dI' % (len(b) // 4), b))

def from_words(w):
    return struct.pack('<%dI' % len(w), *w)

def xxtea(v, k, mode):
    n = len(v)
    if n < 2:
        return v
    kk = list(k)
    rounds = 6 + 52 // n
    if mode == 'sub':
        s = (rounds * DELTA) & MASK
        while s != 0:
            e = (s >> 2) & 3
            for p in range(n - 1, 0, -1):
                z = v[p - 1]
                v[p] = (v[p] - (((z >> 5 ^ v[(p + 1) % n] << 2) + (v[(p + 1) % n] >> 3 ^ z << 4)) ^ ((s ^ v[(p + 1) % n]) + (kk[(p & 3) ^ e] ^ z)))) & MASK
            z = v[n - 1]
            v[0] = (v[0] - (((z >> 5 ^ v[1] << 2) + (v[1] >> 3 ^ z << 4)) ^ ((s ^ v[1]) + (kk[0 ^ e] ^ z)))) & MASK
            s = (s - DELTA) & MASK
        return v
    else:
        s = 0
        for _ in range(rounds):
            e = (s >> 2) & 3
            for p in range(n - 1):
                z = v[p - 1] if p > 0 else v[n - 1]
                v[p] = (v[p] + (((z >> 5 ^ v[(p + 1) % n] << 2) + (v[(p + 1) % n] >> 3 ^ z << 4)) ^ ((s ^ v[(p + 1) % n]) + (kk[(p & 3) ^ e] ^ z)))) & MASK
            z = v[n - 2]
            v[n - 1] = (v[n - 1] + (((z >> 5 ^ v[0] << 2) + (v[0] >> 3 ^ z << 4)) ^ ((s ^ v[0]) + (kk[((n - 1) & 3) ^ e] ^ z)))) & MASK
            s = (s + DELTA) & MASK
        return v

cands = [
    ('f3e08b5119358a8f58f17a678759f60c', 0),
    ('4265ebc749ff7d0f1f1f88232e81632e', 1),
    ('606117a2f4bde428b7458a54b6e87b85', 2),
    ('a20e034bf8813ef5c18d01105e726a17', 3),
    ('eb248b264ae9706f440bedc8ccb6b22c', 4),
]
pad = (-len(body)) % 4
body2 = body + b'\x00' * pad
outdir = r'C:\Users\20751\tomdump\dec_test'
os.makedirs(outdir, exist_ok=True)
for hexs, ci in cands:
    key = bytes.fromhex(hexs)
    k = struct.unpack('<4I', key)
    for mode in ('sub', 'add'):
        v = to_words(body2)
        r = xxtea(v, k, mode)
        rb = from_words(r)
        printable = sum(1 for b in rb[:64] if 32 <= b < 127)
        flag = ' ★★★ Lua!' if rb[:4] == b'\x1bLua' else ''
        if printable > 40 or rb[:4] == b'\x1bLua':
            print(f'候选{ci} {mode}: 可打印{printable}/64 前16B={rb[:16].hex()}{flag}')
        if rb[:4] == b'\x1bLua':
            open(os.path.join(outdir, f'dec_{ci}_{mode}.bin'), 'wb').write(rb)
print('完成')
