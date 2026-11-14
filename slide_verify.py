# -*- coding: utf-8 -*-
# 黄金对滑动验证: 用 common_utils 黄金对验证 sodata/堆中的 16B key 候选
# 分块处理: 每块 1MB, 结果落盘
import struct, sys

PLAIN = r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac'
CIPHER = r'C:\Users\20751\tomdump\device_src\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin'
MASK = 0xffffffff
DELTA = 0x9e3779b9

plain = open(PLAIN, 'rb').read()
cipher = open(CIPHER, 'rb').read()
cdata = cipher[12:]
n = len(cdata) // 4
ref = plain[:n*4]

def xxtea_check(key16):
    """解密并检查前 16B 是否匹配明文头 (快速失败)"""
    k = struct.unpack('<4I', key16)
    v = list(struct.unpack('<%dI' % n, cdata))
    rounds = 6 + 52 // n
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
    out = struct.pack('<%dI' % n, *v)
    return out[:16] == ref[:16]

# 读取候选文件 (sodata / 堆 dump)
import glob, os
files = sys.argv[1:]
print('文件:', files)
for fn in files:
    data = open(fn, 'rb').read()
    print(f'{os.path.basename(fn)}: {len(data)}B, 滑动验证 16B...')
    # 只验证含可打印字符较少的区域? 全滑
    hits = []
    step = 1
    for i in range(0, len(data) - 16, step):
        if i % 1000000 == 0:
            print(f'  ...{i//1048576}MB / {len(data)//1048576}MB', flush=True)
        key16 = data[i:i+16]
        if xxtea_check(key16):
            hits.append((i, key16))
            print(f'  ★★★ 命中 @{hex(i)}: {key16.hex()} {key16!r}')
            break
    print(f'  完成: {len(hits)} 命中')
    if hits:
        open(os.path.basename(fn) + '.KEY', 'wb').write(hits[0][1])
