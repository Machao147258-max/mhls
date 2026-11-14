# -*- coding: utf-8 -*-
"""audit_chunks.py — 审计: 名字字段 → luac头校验 → 结构走查, 统计活缓冲"""
import glob, os, re, struct, json

BASE = r'C:\Users\20751\tomdump\dd_live_1973'
segmap = json.load(open(os.path.join(BASE, 'segmap.json')))

def u32(d, p): return struct.unpack_from('<I', d, p)[0]

def walk(d, p):
    """按 undump 结构走查, 返回 (ok, 结束偏移或错误信息)"""
    try:
        ln = u32(d, p); p += 4
        if ln <= 0 or ln > 2000: return False, 'len=%d' % ln
        p += ln
        p += 4 + 4 + 4
        ncode = u32(d, p); p += 4
        if ncode > 4000000: return False, 'ncode=%d' % ncode
        p += ncode * 4
        nk = u32(d, p); p += 4
        if nk > 1000000: return False, 'nk=%d' % nk
        for i in range(nk):
            t = d[p]; p += 1
            if t == 0: pass
            elif t == 1: p += 1
            elif t == 3: p += 8
            elif t == 4:
                l = u32(d, p); p += 4
                if l <= 0 or l > 100000: return False, 'cstr=%d' % l
                p += l
            else:
                return False, 'ctype=%d' % t
        # debug 段
        n = u32(d, p); p += 4
        if n > 4000000: return False, 'lineinfo'
        p += n
        n = u32(d, p); p += 4
        if n > 1000000: return False, 'locvars'
        for _ in range(n):
            l = u32(d, p); p += 4
            p += l + 8
        n = u32(d, p); p += 4
        if n > 1000000: return False, 'upvnames'
        for _ in range(n):
            l = u32(d, p); p += 4
            p += l
        n = u32(d, p); p += 4
        if n > 100000: return False, 'protos=%d' % n
        for _ in range(n):
            ok, r = walk(d, p)
            if not ok: return False, 'sub:' + str(r)
            p = r
        return True, p
    except Exception as e:
        return False, 'exc:%s' % e

stats = {'total_names': 0, 'clean_header': 0, 'walk_ok': 0}
examples = []
for i in range(len(segmap)):
    fn = os.path.join(BASE, 's%03d.bin' % i)
    if not os.path.exists(fn):
        continue
    d = open(fn, 'rb').read()
    for m in re.finditer(rb'@src/[a-zA-Z0-9_/\.\-]{5,80}\.lua\x00', d):
        stats['total_names'] += 1
        j = m.start()
        # 校验: j-4 是长度, j-16 是 luac 头
        if j < 16:
            continue
        if d[j-4:j-4+4] == b'\x00\x00\x00\x00':
            continue
        ln = u32(d, j-4)
        if ln != m.end() - j:
            continue
        if d[j-16:j-12] != b'\x1b\x4c\x75\x61':
            continue
        stats['clean_header'] += 1
        ok, r = walk(d, j-4)
        if ok:
            stats['walk_ok'] += 1
            if len(examples) < 12:
                examples.append((m.group()[:-1].decode(), r - (j-4)))
print(stats)
for name, size in examples:
    print('  OK', name, size, 'B')