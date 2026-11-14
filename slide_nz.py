# -*- coding: utf-8 -*-
# 非零页滑窗验证 (精确黄金对 UGCSystem), 8 进程
import struct, sys, os
from multiprocessing import Pool

MASK = 0xffffffff
DELTA = 0x9e3779b9
c = open(r'C:\Users\20751\tomdump\pair2\UGCSystem.bin', 'rb').read()
p = open(r'C:\Users\20751\tomdump\mega_luac\src_catchGame_systems_UGCSystem.lua.luac', 'rb').read()
CDATA = c[12:][:len(c[12:])//4*4]
N = len(CDATA)//4
REF = p[:64]
CV = list(struct.unpack('<%dI' % N, CDATA))

def check(key16):
    k = struct.unpack('<4I', key16)
    v = CV[:]
    rounds = 6 + 52 // N
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for i in range(N - 1, 0, -1):
            z = v[i - 1]
            ki = (i ^ e) & 3
            mx = ((((z ^ k[ki]) + (y ^ sumv)) & MASK) ^
                  ((((y >> 3) ^ ((z << 4) & MASK)) + (((y << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[i] = (v[i] - mx) & MASK
            y = v[i]
        z = v[N - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^
               (((y ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    out = struct.pack('<%dI' % N, *v)
    return sum(1 for a, b in zip(out[:64], REF) if a == b) > 48

def worker(args):
    fn, lo, hi = args
    data = open(fn, 'rb').read()
    # 只在非零页内滑
    page = 4096
    for start in range(lo, min(hi, len(data) - 16), page):
        chunk = data[start:start + page]
        if not any(chunk):
            continue
        for i in range(start, min(start + page, len(data) - 16)):
            if check(data[i:i+16]):
                return (fn, i, data[i:i+16])
    return None

if __name__ == '__main__':
    fn = sys.argv[1]
    size = os.path.getsize(fn)
    nproc = 8
    chunk = ((size - 16) // 4096 // nproc) * 4096
    jobs = [(fn, i * chunk, (i + 1) * chunk) for i in range(nproc)]
    jobs[-1] = (fn, (nproc - 1) * chunk, size)
    print(f'{fn}: {size//1048576}MB 非零页滑窗, {nproc} 进程...', flush=True)
    with Pool(nproc) as pool:
        for res in pool.imap_unordered(worker, jobs):
            if res:
                fn2, i, k = res
                print(f'★★★ KEY @{fn2}+{hex(i)}: {k.hex()} {k!r}', flush=True)
                open(r'C:\Users\20751\tomdump\KEY_FOUND.bin', 'wb').write(k)
                pool.terminate()
                raise SystemExit
    print('无命中', flush=True)
