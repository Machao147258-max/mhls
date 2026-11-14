# -*- coding: utf-8 -*-
# 计算 luac 精确结构大小 (parse_end), 验证黄金对
import struct, sys

def rd_tstr(b, p):
    if p + 4 > len(b): return None
    ln = struct.unpack_from('<I', b, p)[0]
    if ln > 0x100000: return None
    p += 4
    if ln == 0: return b'', p
    if p + ln > len(b): return None
    return b[p:p+ln-1], p + ln

def parse(b, p):
    r = rd_tstr(b, p)
    if r is None: return None
    _, p = r
    if p + 16 > len(b): return None
    p += 12
    if p + 4 > len(b): return None
    sc = struct.unpack_from('<I', b, p)[0]
    if sc > 0x1000000: return None
    p += 4 + sc * 4
    if p + 4 > len(b): return None
    sizek = struct.unpack_from('<I', b, p)[0]
    if sizek > 0x100000: return None
    p += 4
    for i in range(sizek):
        if p >= len(b): return None
        t = b[p]; p += 1
        if t == 0: pass
        elif t == 1: p += 1
        elif t == 3: p += 8
        elif t == 4:
            r = rd_tstr(b, p)
            if r is None: return None
            _, p = r
        else: return None
    if p + 4 > len(b): return None
    sizep = struct.unpack_from('<I', b, p)[0]
    if sizep > 0x100000: return None
    p += 4
    for i in range(sizep):
        r = parse(b, p)
        if r is None: return None
        p = r
    if p + 4 > len(b): return None
    nli = struct.unpack_from('<I', b, p)[0]
    if nli > 0x1000000: return None
    p += 4 + nli * 4
    if p + 4 > len(b): return None
    nlv = struct.unpack_from('<I', b, p)[0]
    if nlv > 0x100000: return None
    p += 4
    for _ in range(nlv):
        r = rd_tstr(b, p)
        if r is None: return None
        _, p = r
        p += 8
    if p + 4 > len(b): return None
    nuv = struct.unpack_from('<I', b, p)[0]
    if nuv > 0x100000: return None
    p += 4
    for _ in range(nuv):
        r = rd_tstr(b, p)
        if r is None: return None
        _, p = r
    return p

import os, glob
for f in sorted(glob.glob(r'C:\Users\20751\tomdump\mega_luac\*.luac')):
    try:
        b = open(f, 'rb').read()
        ln = struct.unpack_from('<I', b, 12)[0]
        src = b[16:16+ln-1]
        end = parse(b, 12)
        print(f'{os.path.basename(f):60s} {len(b):9d}B  parse_end={end}  结构大小={end-12 if end else "-"}')
    except Exception as e:
        print(f, 'ERR', e)
