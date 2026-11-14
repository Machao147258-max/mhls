# -*- coding: utf-8 -*-
# 组合搜索: 密文偏移(8/12/16) × 轮数(6/32/52) × n 对齐
import struct

plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac','rb').read()
cipher = open(r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin','rb').read()
MASK = 0xffffffff
DELTA = 0x9e3779b9

def solve_k(mx, z, y, s):
    C1 = ((y >> 3) ^ ((z << 4) & MASK)) & MASK
    C2 = ((y << 2) & MASK) ^ (z >> 5)
    B = (y ^ s) & MASK
    zbits = [(z >> i) & 1 for i in range(32)]
    Bbits = [(B >> i) & 1 for i in range(32)]
    C1b = [(C1 >> i) & 1 for i in range(32)]
    C2b = [(C2 >> i) & 1 for i in range(32)]
    MXb = [(mx >> i) & 1 for i in range(32)]
    cands = [(0, 0, 0)]
    for i in range(32):
        new = []
        for kb, ca, cb in cands:
            for ki in (0, 1):
                A = zbits[i] ^ ki
                ai = A ^ Bbits[i] ^ ca
                ca2 = ((A & Bbits[i]) | (A & ca) | (Bbits[i] & ca))
                bi = C1b[i] ^ C2b[i] ^ cb
                cb2 = ((C1b[i] & C2b[i]) | (C1b[i] & cb) | (C2b[i] & cb))
                if (ai ^ bi) == MXb[i]:
                    new.append((kb | (ki << i), ca2, cb2))
        cands = new
        if not cands:
            return None
    return cands[0][0]

def decrypt(data, k, rounds):
    n = len(data) // 4
    v = list(struct.unpack('<%dI' % n, data))
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            mx = ((((z ^ k[ki]) + (y ^ sumv)) & MASK) ^
                  ((((y >> 3) ^ ((z << 4) & MASK)) + (((y << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[p] = (v[p] - mx) & MASK
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^
               (((y ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    return struct.pack('<%dI' % n, *v)

for off in [8, 12, 16]:
    for rmode in ['6+52n', '32', '52n']:
        cdata = cipher[off:]
        # 4 对齐
        cdata = cdata[:len(cdata)//4*4]
        n = len(cdata) // 4
        if n < 2: continue
        if rmode == '6+52n': rounds = 6 + 52 // n
        elif rmode == '32': rounds = 32
        else: rounds = max(1, 52 // n)
        sum0 = (rounds * DELTA) & MASK
        e = (sum0 >> 2) & 3
        v_c = list(struct.unpack('<%dI' % n, cdata))
        # 明文可能从 luac 的某字偏移开始 (0..3 字)!
        for pskip in range(0, 4):
            pbytes = plain[pskip*4:pskip*4+n*4]
            if len(pbytes) < n*4:
                pbytes = pbytes.ljust(n*4, b'\x00')
            v_p = list(struct.unpack('<%dI' % n, pbytes))
            # 反推
            kw = {}
            ok = True
            y = v_c[0]
            for p in range(n - 1, 0, -1):
                z = v_c[p - 1]
                mx = (v_c[p] - v_p[p]) & MASK
                ki = (p ^ e) & 3
                k = solve_k(mx, z, y, sum0)
                if k is None:
                    ok = False; break
                if ki in kw and kw[ki] != k:
                    ok = False; break
                kw[ki] = k
                y = v_p[p]
            if not ok or len(kw) < 4:
                continue
            key = struct.pack('<4I', kw[0], kw[1], kw[2], kw[3])
            # 验证
            dec = decrypt(cdata, list(struct.unpack('<4I', key)), rounds)
            score = sum(1 for a, b in zip(dec[:64], plain[:64]) if a == b)
            print(f'off={off} {rmode} pskip={pskip}: n={n} rounds={rounds} score={score}/64 KEY={key.hex()}')
            if dec.startswith(b'\x1bLuaQ'):
                print('  🎉🎉🎉 成功!!')
                open(r'C:\Users\20751\tomdump\DECRYPTED_FINAL.luac', 'wb').write(dec)
                raise SystemExit
print('done')