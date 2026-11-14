# -*- coding: utf-8 -*-
# MD5(候选字符串) 批量测试 84B 小文件 (最快验证)
import struct, hashlib

data = open(r'C:\Users\20751\tomdump\apk_launcher\2245023265ae4cf87d02c8b6ba991139.bin', 'rb').read()
MASK = 0xffffffff; DELTA = 0x9e3779b9

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

# 候选字符串
import re
cands = [
    b'ioscacheudid', b'X1V5fzTo', b'userext', b'Crypto', b'MD5',
    b'com.netease.tom', b'netease', b'netease.tom', b'tom',
    b'7.45.0', b'launcher', b'launcher.lua', b'main.lua',
    b'filelist', b'filelist_high.json', b'filelist_base.json',
    b'X1V5fzToX1V5fzTo', b'h18', b'h18v6', b'update.netease.com',
    b'h18.gph.netease.com', b'mumu', b'android', b'dev',
    b'encryptString', b'decryptStringWithKeyLua', b'encryptStringWithKeyLua',
    b'getKey', b'setKey', b'XXTEAUtil', b'xxtea', b'tea',
]
# 加 launcher 全部常量
try:
    txt = open(r'C:\Users\20751\Desktop\猫和老鼠\launcher_consts.txt', encoding='utf-8', errors='replace').read()
    for m in re.finditer(rb"k:\s*b'([^']+)'", txt.encode('latin-1')):
        cands.append(m.group(1)[:64])
except Exception:
    pass
print('候选字符串:', len(cands))

def test_key(key, name):
    k = struct.unpack('<4I', key[:16].ljust(16, b'\x00'))
    for off in (12, 16):
        body = data[off:]
        pad = (-len(body)) % 4
        body2 = body + b'\x00' * pad
        for mode, fn in [('sub', decrypt_sub), ('add', encrypt_add)]:
            r = fn(body2, k)
            pr = sum(1 for b in r if 32 <= b < 127)
            if pr >= len(r) * 0.6 or r[:4] == b'\x1bLua':
                print(f'★★★ {name} {mode} off={off}: {r!r}')
                return True
    return False

hit = False
for c in cands:
    if hit: break
    for vname, v in [('raw', hashlib.md5(c).digest()), ('hex16', hashlib.md5(c).hexdigest()[:16].encode()), ('hex32', hashlib.md5(c).hexdigest().encode())]:
        if test_key(v, f'MD5({c[:20]}){vname}'):
            hit = True
            break
    # 也直接测字符串本身 (16B 截断/补零)
    if test_key(c[:16].ljust(16, b'\x00'), f'str:{c[:16]}'):
        hit = True
print('完成, 命中:', hit)
