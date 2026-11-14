# -*- coding: utf-8 -*-
# UGCSystem 精确黄金对滑窗验证多个内存 dump
import struct, sys, time

MASK = 0xffffffff
DELTA = 0x9e3779b9
c = open(r'C:\Users\20751\tomdump\pair2\UGCSystem.bin', 'rb').read()
p = open(r'C:\Users\20751\tomdump\mega_luac\src_catchGame_systems_UGCSystem.lua.luac', 'rb').read()

def check(key16):
    cdata = c[12:]
    cdata = cdata[:len(cdata)//4*4]
    n = len(cdata)//4
    if n < 2:
        return False
    k = struct.unpack('<4I', key16)
    v = list(struct.unpack('<%dI' % n, cdata))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for i in range(n - 1, 0, -1):
            z = v[i - 1]
            ki = (i ^ e) & 3
            mx = ((((z ^ k[ki]) + (y ^ sumv)) & MASK) ^
                  ((((y >> 3) ^ ((z << 4) & MASK)) + (((y << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[i] = (v[i] - mx) & MASK
            y = v[i]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^
               (((y ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    out = struct.pack('<%dI' % n, *v)
    return sum(1 for a, b in zip(out[:64], p[:64]) if a == b) > 48

files = sys.argv[1:]
print('滑窗验证:', files)
for fn in files:
    data = open(fn, 'rb').read()
    print(f'{fn}: {len(data)//1024}KB...', flush=True)
    t0 = time.time()
    hit = None
    for i in range(0, len(data) - 16):
        if check(data[i:i+16]):
            hit = (i, data[i:i+16])
            break
        if i % 200000 == 0 and i:
            pass
    if hit:
        i, k = hit
        print(f'  ★★★ 命中 @{hex(i)}: {k.hex()} {k!r}')
        open(r'C:\Users\20751\tomdump\KEY_FOUND.bin', 'wb').write(k)
        raise SystemExit
    print(f'  无命中 ({time.time()-t0:.0f}s)')
print('=== 完成 ===')
