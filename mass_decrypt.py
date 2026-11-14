# -*- coding: utf-8 -*-
# 批量解密: X1V5fzTo + 4B随机 + XXTEA (标准解密, 与 0x8526a8 一致)
# 用法: python mass_decrypt.py <key_hex或文件> <输入目录> <输出目录>
import struct, os, sys

MASK32 = 0xffffffff
DELTA = 0x9e3779b9
LUAC = b'\x1bLua'

def decrypt(data, key):
    n = len(data) // 4
    if n < 2: return None
    v = list(struct.unpack('<%dI' % n, data))
    k = list(struct.unpack('<4I', key.ljust(16, b'\x00')[:16]))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK32
    if sumv == 0: return None
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            mx = ((((z ^ k[ki]) + (y ^ sumv)) & MASK32) ^
                  ((((y >> 3) ^ ((z << 4) & MASK32)) + (((y << 2) & MASK32) ^ (z >> 5))) & MASK32)) & MASK32
            v[p] = (v[p] - mx) & MASK32
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK32)) + (((z << 4) & MASK32) ^ (y >> 3))) & MASK32) ^
               (((y ^ sumv) + (z ^ k[ki])) & MASK32)) & MASK32
        v[0] = (v[0] - mx0) & MASK32
        sumv = (sumv - DELTA) & MASK32
    return struct.pack('<%dI' % n, *v)

def main():
    key_arg, src, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    if os.path.exists(key_arg) and os.path.getsize(key_arg) <= 16:
        key = open(key_arg, 'rb').read()
    else:
        key = bytes.fromhex(key_arg.replace('0x', ''))
    print(f'key={key.hex()} src={src} → {dst}', flush=True)
    os.makedirs(dst, exist_ok=True)
    stats = {'ok': 0, 'luac': 0, 'fail': 0, 'other': 0}
    for root, dirs, files in os.walk(src):
        for fn in files:
            if not fn.endswith('.bin'): continue
            p = os.path.join(root, fn)
            data = open(p, 'rb').read()
            if data[:8] != b'X1V5fzTo':
                stats['other'] += 1
                continue
            cdata = data[12:]
            n = len(cdata) // 4
            cdata = cdata[:n*4]
            body = decrypt(cdata, key)
            if body is None:
                stats['fail'] += 1
                continue
            stats['ok'] += 1
            if body[:4] == LUAC:
                stats['luac'] += 1
            rel = os.path.relpath(p, src).replace('\\', '_').replace('/', '_')
            open(os.path.join(dst, rel + '.dec'), 'wb').write(body)
    print(stats, flush=True)

if __name__ == '__main__':
    main()
