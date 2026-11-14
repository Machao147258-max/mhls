# -*- coding: utf-8 -*-
# 终极滑窗: heap_cur/900a6d9000.bin (main.lua 所在堆块) 全部 16B 候选 × xxtea 测试
import struct, multiprocessing, os

BUF = open(r'C:\Users\20751\tomdump\heap_cur\900a6d9000.bin', 'rb').read()
TESTF = r'C:\Users\20751\tomdump\apk_launcher\2245023265ae4cf87d02c8b6ba991139.bin'
TDATA = open(TESTF, 'rb').read()
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

# 预生成 body2 (off 12/16)
bodys = {}
for off in (12, 16):
    body = TDATA[off:]
    pad = (-len(body)) % 4
    bodys[off] = body + b'\x00' * pad

def worker(rng):
    hits = []
    for off in rng:
        b = BUF[off:off+16]
        if len(b) < 16: continue
        if b == b'\x00'*16 or b == b'\xff'*16: continue
        nz = sum(1 for x in b if x != 0)
        if nz < 10: continue
        ac = sum(1 for x in b if 32 <= x < 127)
        if ac > 6: continue
        v8 = struct.unpack_from('<Q', b)[0]
        if 0x400000000000 <= v8 < 0x800000000000: continue
        if 0x900000000000 <= v8 < 0xa00000000000: continue
        k = struct.unpack('<4I', b)
        for mode_off in (12, 16):
            try:
                r = encrypt_add(bodys[mode_off], k)
            except Exception:
                continue
            pr = sum(1 for x in r if 32 <= x < 127)
            if r[:4] == b'\x1bLua' or (len(r) <= 100 and pr >= len(r) * 0.6):
                hits.append((off, b.hex(), mode_off, r[:24]))
    return hits

def main():
    total = len(BUF) - 16
    print('滑窗范围:', total, '候选(粗筛后约 1/8)')
    nproc = 8
    step = total // nproc
    ranges = [range(i*step, (i+1)*step if i < nproc-1 else total) for i in range(nproc)]
    pool = multiprocessing.Pool(nproc)
    results = pool.map(worker, ranges)
    pool.close()
    allhits = []
    for r in results:
        allhits.extend(r)
    print('命中:', len(allhits))
    for h in allhits:
        print('  ★ off=%#x key=%s off=%d out=%s' % h)

if __name__ == '__main__':
    main()
