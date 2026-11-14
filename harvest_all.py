# -*- coding: utf-8 -*-
# 全量: 所有 dd bin 的所有 1bLuaQ 头 → 解析 → 提取
import os, struct

OUT = r'C:\Users\20751\tomdump\harvest3'
os.makedirs(OUT, exist_ok=True)

def rd_tstr(b, p):
    if p + 4 > len(b): return None, p
    ln = struct.unpack_from('<I', b, p)[0]
    if ln == 0 or ln > 0x100000: return b'', p + 4
    if p + 4 + ln > len(b): return None, p
    return b[p+4:p+4+ln-1], p + 4 + ln

def parse_proto_size(b, p, depth=0):
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
        # 容错: debug 段异常时, 找下一个 0x00000000 后继续 (保守)
        try:
            for q in range(p, min(p + 64, len(b) - 4)):
                if struct.unpack_from('<I', b, q)[0] == 0:
                    return src, q + 4
        except Exception:
            pass
        return None
    return src, p

dirs = [r'C:\Users\20751\tomdump\dd_live_1973', r'C:\Users\20751\tomdump\sweep_1973\r1', r'C:\Users\20751\tomdump\sweep_1973\r2', r'C:\Users\20751\tomdump\sweep_1973\r3']
saved = 0
seen_names = {}
for d in dirs:
    if not os.path.isdir(d): continue
    for f in sorted(os.listdir(d)):
        p = os.path.join(d, f)
        if os.path.isdir(p): continue
        try:
            b = open(p, 'rb').read()
        except Exception:
            continue
        pos = 0
        while True:
            i = b.find(b'\x1bLuaQ', pos)
            if i < 0: break
            r = parse_proto_size(b, i + 12)
            if r:
                src, end = r
                sz = end - i
                if sz > 100:
                    sname = src.decode('utf-8', 'replace').replace('/', '__').replace('@', '')[:80]
                    sname = ''.join(c if c.isalnum() or c in '._-' else '_' for c in sname)
                    key = sname
                    # 去重: 同名保留最大
                    if key not in seen_names or sz > seen_names[key][0]:
                        seen_names[key] = (sz, b[i:end])
                    pos = end
                    continue
            pos = i + 1
print('唯一脚本:', len(seen_names))
for name, (sz, data) in sorted(seen_names.items()):
    fn = os.path.join(OUT, name + '.luac')
    try:
        open(fn, 'wb').write(data)
        saved += 1
        print('  %s (%dB)' % (name, sz))
    except Exception as e:
        print('  X %s: %s' % (name, e))
print('保存:', saved)
