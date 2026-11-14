# -*- coding: utf-8 -*-
# 扫描 launcher 所有子函数常量: 找 decryptStringWithKeyLua / 16B key / 加密相关
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()

def rd_tstr(pos):
    if pos + 4 > len(buf): return None, pos
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0 or ln > 0x100000: return b'', pos + 4
    if pos + 4 + ln > len(buf): return None, pos
    return buf[pos+4:pos+4+ln-1], pos + 4 + ln

all_fns = []
def walk(pos, depth, path):
    r = rd_tstr(pos)
    if r[0] is None: return None
    _, pos = r
    pos += 12
    if pos + 4 > len(buf): return None
    sc = struct.unpack_from('<I', buf, pos)[0]
    if sc > 0x100000: return None
    pos += 4 + sc * 4
    if pos + 4 > len(buf): return None
    sizek = struct.unpack_from('<I', buf, pos)[0]
    if sizek > 0x100000: return None
    pos += 4
    ks = []
    for i in range(sizek):
        if pos >= len(buf): return None
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1:
            if pos >= len(buf): return None
            ks.append(bool(buf[pos])); pos += 1
        elif t == 3:
            if pos + 8 > len(buf): return None
            ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            rr = rd_tstr(pos)
            if rr[0] is None: return None
            ks.append(rr[0]); pos = rr[1]
        else:
            return None
    if pos + 4 > len(buf): return None
    sizep = struct.unpack_from('<I', buf, pos)[0]
    if sizep > 0x100000: return None
    pos += 4
    for i in range(sizep):
        r = walk(pos, depth+1, path + '.' + str(i))
        if r is None: return None
        pos = r
    # debug 容错
    try:
        n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if n > 0x1000000: return None
        pos += n * 4
        n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if n > 0x100000: return None
        for _ in range(n):
            rr = rd_tstr(pos)
            if rr[0] is None: return None
            _, pos = rr
            pos += 8
        n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if n > 0x100000: return None
        for _ in range(n):
            rr = rd_tstr(pos)
            if rr[0] is None: return None
            _, pos = rr
    except Exception:
        return None
    all_fns.append((path, ks, sc))
    return pos

walk(12, 0, 'main')
print('解析到 %d 个函数' % len(all_fns))
print()
kw = [b'crypt', b'key', b'x1v5', b'md5', b'secret', b'token', b'sign', b'udid']
for path, ks, sc in all_fns:
    hits = []
    for k in ks:
        if isinstance(k, bytes):
            kl = k.lower()
            if any(x in kl for x in kw):
                hits.append(k)
            elif len(k) == 16 and all(32 <= c < 127 for c in k):
                hits.append(b'16B-ASCII: ' + k)
            elif len(k) == 16 and any(c == 0 for c in k):
                hits.append(b'16B-bin')
    if hits:
        print('fn %s sc=%d k=%d:' % (path, sc, len(ks)))
        for h in hits[:12]:
            print('    %r' % h)
