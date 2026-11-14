# -*- coding: utf-8 -*-
# 多进程测试 s542 高熵候选 (84B 文件, add 方向 12/16 偏移)
import struct, multiprocessing, os, sys

data = open(r'C:\Users\20751\tomdump\apk_launcher\2245023265ae4cf87d02c8b6ba991139.bin', 'rb').read()
MASK = 0xffffffff
DELTA = 0x9e3779b9

def encrypt_add(body2, k):
    n = len(body2) // 4
    if n < 2: return body2
    v = list(struct.unpack('<%dI' % n, body2))
    rounds = 6 + 52 // n
    sumv = 0
    for _ in range(rounds):
        sumv = (sumv + DELTA) & MASK
        e = sumv >> 2
        z = v[n - 1]
        for p in range(n - 1):
            y = v[p + 1]
            ki = (p ^ e) & 3
            mx = ((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^ (((z ^ sumv) + (z ^ k[ki])) & MASK)
            v[p] = (v[p] + mx) & MASK
            z = v[p]
        y = v[0]
        ki = ((n - 1) ^ e) & 3
        mx0 = ((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^ (((y ^ sumv) + (y ^ k[ki])) & MASK)
        v[n - 1] = (v[n - 1] + mx0) & MASK
    return struct.pack('<%dI' % n, *v)

def worker(chunk):
    hits = []
    for hexs, off_hint in chunk:
        try:
            key = bytes.fromhex(hexs)
        except Exception:
            continue
        k = struct.unpack('<4I', key[:16].ljust(16, b'\x00'))
        for off in (12, 16):
            body = data[off:]
            pad = (-len(body)) % 4
            body2 = body + b'\x00' * pad
            try:
                r = encrypt_add(body2, k)
            except Exception:
                continue
            pr = sum(1 for b in r if 32 <= b < 127)
            if r[:4] == b'\x1bLua' or (len(r) <= 100 and pr >= len(r) * 0.6):
                hits.append((hexs, off, r[:32]))
    return hits

def main():
    cands = []
    for line in open(r'C:\Users\20751\tomdump\s542_key_cands.txt'):
        hexs, off = line.split()
        cands.append((hexs, int(off, 16)))
    print('候选:', len(cands))
    nproc = 8
    chunks = [cands[i::nproc] for i in range(nproc)]
    pool = multiprocessing.Pool(nproc)
    results = pool.map(worker, chunks)
    pool.close()
    allhits = []
    for r in results:
        allhits.extend(r)
    print('命中:', len(allhits))
    for h in allhits:
        print('  ★', h)

if __name__ == '__main__':
    main()
