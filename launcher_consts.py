# -*- coding: utf-8 -*-
# 提取 launcher_raw.luac 所有函数的常量表, 找 key 字符串
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()

def rd_tstr(pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

def walk(pos, depth, fidx):
    ln = struct.unpack_from('<I', buf, pos)[0]
    src, pos = rd_tstr(pos)
    pos += 12
    sc = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    pos += sc * 4
    sizek = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    ks = []
    for i in range(sizek):
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(bool(buf[pos])); pos += 1
        elif t == 3: ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            s, pos = rd_tstr(pos); ks.append(s)
        else:
            raise ValueError(f'const type {t}')
    sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    print(f'{"  "*depth}fn#{fidx} src={src!r} sc={sc} k={sizek} protos={sizep}')
    for s in ks:
        if isinstance(s, bytes) and len(s) >= 4:
            print(f'{"  "*depth}   k: {s!r}')
    for i in range(sizep):
        pos = walk(pos, depth+1, i)
    # debug
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    pos += n * 4
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos); pos += 8
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos)
    return pos

try:
    walk(12, 0, 0)
except ValueError as e:
    print('✗', e)
