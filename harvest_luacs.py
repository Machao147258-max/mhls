# -*- coding: utf-8 -*-
# 批量从所有 dump 提取完整 luac (带头格式) 并识别 source 名
import os, struct, glob

OUT = r'C:\Users\20751\tomdump\harvest'
os.makedirs(OUT, exist_ok=True)

def rd_tstr(b, p):
    if p + 4 > len(b): return None, p
    ln = struct.unpack_from('<I', b, p)[0]
    if ln == 0 or ln > 0x100000: return b'', p + 4
    if p + 4 + ln > len(b): return None, p
    return b[p+4:p+4+ln-1], p + 4 + ln

def parse_proto_size(b, p, depth=0):
    """返回 (source名, 消耗字节) 或 None"""
    if depth > 60: return None
    r = rd_tstr(b, p)
    if r[0] is None: return None
    src, p = r
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
            if r[0] is None: return None
            p = r[1]
        else:
            return None
    if p + 4 > len(b): return None
    sizep = struct.unpack_from('<I', b, p)[0]
    if sizep > 0x100000: return None
    p += 4
    for i in range(sizep):
        r = parse_proto_size(b, p, depth + 1)
        if r is None: return None
        p = r[1]
    # debug
    try:
        n = struct.unpack_from('<I', b, p)[0]
        if n > 0x1000000: return None
        p += 4 + n * 4
        n = struct.unpack_from('<I', b, p)[0]
        if n > 0x100000: return None
        p += 4
        for _ in range(n):
            r = rd_tstr(b, p)
            if r[0] is None: return None
            _, p = r
            p += 8
        n = struct.unpack_from('<I', b, p)[0]
        if n > 0x100000: return None
        p += 4
        for _ in range(n):
            r = rd_tstr(b, p)
            if r[0] is None: return None
            _, p = r
    except Exception:
        return None
    return src, p

# 扫描所有 bin
roots = [r'C:\Users\20751\tomdump\dd_live_1973', r'C:\Users\20751\tomdump\sweep_1973']
found = []
for root in roots:
    for f in sorted(os.listdir(root)):
        p = os.path.join(root, f)
        try:
            b = open(p, 'rb').read()
        except Exception:
            continue
        # 找所有 1bLuaQ 头
        pos = 0
        while True:
            i = b.find(b'\x1bLuaQ', pos)
            if i < 0:
                break
            # 尝试从 i+12 解析
            r = parse_proto_size(b, i + 12)
            if r:
                src, end = r
                if end - i > 100:  # 足够大
                    found.append((p, i, end, src))
                    pos = end
                    continue
            pos = i + 1
print('找到 luac:', len(found))
# 去重 (同 source 保留最大)
by_src = {}
for p, i, end, src in found:
    key = (os.path.basename(p), src)
    sz = end - i
    if key not in by_src or sz > by_src[key][2]:
        by_src[key] = (p, i, end, sz)
print('去重后:', len(by_src))
saved = 0
for (bf, src), (p, i, end, sz) in sorted(by_src.items()):
    b = open(p, 'rb').read()
    data = b[i:end]
    safe = src.decode('utf-8', 'replace').replace('/', '__').replace('@', '').replace('\\', '_')[:80] or 'unknown'
    fn = os.path.join(OUT, '%s__%s.luac' % (os.path.basename(p).replace('.bin', ''), safe))
    try:
        open(fn, 'wb').write(data)
        saved += 1
        print('  %s (%dB) <- %s@%#x' % (safe, sz, bf, i))
    except Exception as e:
        print('  保存失败', safe, e)
print('保存:', saved)
