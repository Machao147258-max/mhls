# -*- coding: utf-8 -*-
# 批量: live_segs 全部 bin 扫描 @src 字符串 + 解析序列化 luac
import struct, os, glob

def rd_tstr(buf, pos):
    if pos + 4 > len(buf): return None, pos
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0 or ln > 0x100000: return b'', pos + 4
    if pos + 4 + ln > len(buf): return None, pos
    return buf[pos+4:pos+4+ln-1], pos + 4 + ln

def parse_end(buf, pos, depth=0):
    try:
        if pos + 4 > len(buf): return None
        ln = struct.unpack_from('<I', buf, pos)[0]
        if ln > 0x100000: return None
        src, pos = rd_tstr(buf, pos)
        pos += 12
        if pos + 4 > len(buf): return None
        sc = struct.unpack_from('<I', buf, pos)[0]
        if sc > 0x400000: return None
        pos += 4 + sc * 4
        if pos + 4 > len(buf): return None
        sizek = struct.unpack_from('<I', buf, pos)[0]
        if sizek > 0x100000: return None
        pos += 4
        for _ in range(sizek):
            if pos >= len(buf): return None
            t = buf[pos]; pos += 1
            if t == 0: pass
            elif t == 1: pos += 1
            elif t == 3: pos += 8
            elif t == 4:
                r = rd_tstr(buf, pos)
                if r[0] is None: return None
                pos = r[1]
            else:
                return None
        if pos + 4 > len(buf): return None
        sizep = struct.unpack_from('<I', buf, pos)[0]
        if sizep > 0x100000: return None
        pos += 4
        for _ in range(sizep):
            e = parse_end(buf, pos, depth + 1)
            if e is None: return None
            pos = e
        for field in range(3):
            if pos + 4 > len(buf): return None
            n = struct.unpack_from('<I', buf, pos)[0]
            if n > 0x1000000: return None
            pos += 4
            if field == 0:
                pos += n * 4
            elif field == 1:
                for _ in range(n):
                    r = rd_tstr(buf, pos)
                    if r[0] is None: return None
                    _, pos = r
                    pos += 8
            else:
                for _ in range(n):
                    r = rd_tstr(buf, pos)
                    if r[0] is None: return None
                    _, pos = r
        return pos
    except Exception:
        return None

OUT = r'C:\Users\20751\tomdump\harvest2'
os.makedirs(OUT, exist_ok=True)
saved = 0
for f in sorted(os.listdir(r'C:\Users\20751\tomdump\live_segs')):
    if not f.endswith('.bin'): continue
    p = os.path.join(r'C:\Users\20751\tomdump\live_segs', f)
    b = open(p, 'rb').read()
    # 找所有 @src 前缀 (带长度?)
    found = []
    pos = 0
    while True:
        i = b.find(b'@src/', pos)
        if i < 0: break
        # 尝试往前 4B 作为长度
        ln = struct.unpack_from('<I', b, i - 4)[0] if i >= 4 else 0
        if 4 < ln < 200:
            start = i - 4
        else:
            start = i
        r = parse_end(b, start)
        if r:
            src = b[i:i+60].split(b'\x00')[0].decode('utf-8', 'replace')
            sz = r - start
            if sz > 200:
                found.append((start, r, src, sz))
                pos = r
                continue
        pos = i + 1
    if found:
        print(f'=== {f}: {len(found)} 个 luac ===')
        for start, end, src, sz in found:
            data = b[start:end]
            safe = src.replace('/', '__').replace('@', '')
            fn = os.path.join(OUT, f'{f.replace(".bin","")}__{safe}.luac')
            open(fn, 'wb').write(data)
            print(f'  {src} ({sz}B)')
            saved += 1
print('保存:', saved)
