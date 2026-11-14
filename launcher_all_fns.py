# -*- coding: utf-8 -*-
# 修复版: 解析全部 112 子函数 (跳过损坏的 debug 段), 找 Crypto/decrypt/key
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()

def rd_tstr(pos):
    if pos + 4 > len(buf): return None, pos
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0 or ln > 0x100000: return b'', pos + 4
    if pos + 4 + ln > len(buf): return None, pos
    return buf[pos+4:pos+4+ln-1], pos + 4 + ln

fns = []
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
    ok = True
    for i in range(sizek):
        if pos >= len(buf): ok = False; break
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1:
            if pos >= len(buf): ok = False; break
            ks.append(bool(buf[pos])); pos += 1
        elif t == 3:
            if pos + 8 > len(buf): ok = False; break
            ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            rr = rd_tstr(pos)
            if rr[0] is None: ok = False; break
            ks.append(rr[0]); pos = rr[1]
        else:
            ok = False; break
    if not ok: return None
    if pos + 4 > len(buf): return None
    sizep = struct.unpack_from('<I', buf, pos)[0]
    if sizep > 0x100000: return None
    pos += 4
    for i in range(sizep):
        r = walk(pos, depth + 1, path + '.' + str(i))
        if r is None: return None
        pos = r
    # debug 段: 失败则尝试跳过 (找到下一个 0x00000000 对齐?)
    try:
        n = struct.unpack_from('<I', buf, pos)[0]
        if n > 0x1000000: return None
        pos += 4 + n * 4
        n = struct.unpack_from('<I', buf, pos)[0]
        if n > 0x100000: return None
        pos += 4
        for _ in range(n):
            rr = rd_tstr(pos)
            if rr[0] is None: return None
            _, pos = rr
            pos += 8
        n = struct.unpack_from('<I', buf, pos)[0]
        if n > 0x100000: return None
        pos += 4
        for _ in range(n):
            rr = rd_tstr(pos)
            if rr[0] is None: return None
            _, pos = rr
    except Exception:
        return None
    fns.append((path, ks, sc))
    return pos

walk(12, 0, 'main')
print('解析到 %d 个函数' % len(fns))
kw = [b'crypt', b'key', b'x1v5', b'md5', b'secret', b'token', b'udid', b'launcher_ver', b'filelist', b'download', b'decode', b'encode']
for path, ks, sc in fns:
    hits = []
    for k in ks:
        if isinstance(k, bytes):
            kl = k.lower()
            if any(x in kl for x in kw):
                hits.append(k)
            elif len(k) == 16:
                hits.append(b'16B: ' + k.hex().encode())
    if hits:
        print('fn %s sc=%d k=%d:' % (path, sc, len(ks)))
        for h in hits[:14]:
            print('    %r' % h)
