# -*- coding: utf-8 -*-
# 批量: apk_launcher 8 文件 × 候选 key × 方向 × 偏移 → 找可读/Lua 头
import struct, hashlib, os, glob

MASK = 0xffffffff
DELTA = 0x9e3779b9

def decrypt_sub(data, k):
    n = len(data) // 4
    if n < 2: return data
    v = list(struct.unpack('<%dI' % n, data))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            mx = ((((z ^ k[ki]) + (z ^ sumv)) & MASK) ^ ((((z >> 3) ^ ((z << 4) & MASK)) + (((z << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[p] = (v[p] - mx) & MASK
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^ (((z ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    return struct.pack('<%dI' % n, *v)

def encrypt_add(data, k):
    n = len(data) // 4
    if n < 2: return data
    v = list(struct.unpack('<%dI' % n, data))
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

X = b'X1V5fzTo'
md5u = hashlib.md5(b'ioscacheudid').digest()
md5u_hex = hashlib.md5(b'ioscacheudid').hexdigest()
md5x = hashlib.md5(X).digest()
keys = {
    'md5udid': md5u,
    'md5udid_hex16': md5u_hex[:16].encode(),
    'md5udid_hex32': md5u_hex.encode(),
    'md5X': md5x,
    'X+0': X + b'\x00' * 8,
    'X*2': X * 2,
    'X+md5X8': X + md5x[:8],
    'md5X+X8': md5x + X[:8],
    'X+md5u8': X + md5u[:8],
    'md5u+X8': md5u + X[:8],
    '6bb4': bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b'),
    'KEY.bin': bytes.fromhex('53309dfd1b44b11c51df5763e832b73a'),
    'so_f3e0': bytes.fromhex('f3e08b5119358a8f58f17a678759f60c'),
    'so_4265': bytes.fromhex('4265ebc749ff7d0f1f1f88232e81632e'),
    'so_6061': bytes.fromhex('606117a2f4bde428b7458a54b6e87b85'),
    'so_a20e': bytes.fromhex('a20e034bf8813ef5c18d01105e726a17'),
    'so_eb24': bytes.fromhex('eb248b264ae9706f440bedc8ccb6b22c'),
}

files = sorted(glob.glob(r'C:\Users\20751\tomdump\apk_launcher\*'))
print('文件:', [os.path.basename(f) for f in files])
hits = 0
for fp in files:
    data = open(fp, 'rb').read()
    fn = os.path.basename(fp)
    for off in (12, 16):
        body = data[off:]
        if len(body) < 8: continue
        pad = (-len(body)) % 4
        body2 = body + b'\x00' * pad
        for kn, key in keys.items():
            k = struct.unpack('<4I', key[:16].ljust(16, b'\x00'))
            for mode, fnx in [('sub', decrypt_sub), ('add', encrypt_add)]:
                try:
                    r = fnx(body2, k)
                    pr = sum(1 for b in r[:min(64, len(r))] if 32 <= b < 127)
                    luahdr = r[:4] == b'\x1bLua'
                    # 小文件: 可读性 > 50%
                    small_ok = len(r) <= 100 and pr >= len(r) * 0.6
                    if luahdr or (pr > 40 and not luahdr) or small_ok:
                        hits += 1
                        print(f'★ {fn} off={off} {kn} {mode}: 可打印{pr}/{min(64,len(r))} 前24={r[:24].hex()} str={r[:24]}')
                        if luahdr:
                            out = r'C:\Users\20751\tomdump\dec_' + fn + '_HIT.bin'
                            open(out, 'wb').write(r)
                            print('   ★★★ LUA! saved', out)
                except Exception:
                    pass
print('命中数:', hits)
