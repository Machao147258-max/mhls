# -*- coding: utf-8 -*-
# 提取 x1_enc 段 3 个 luac 完整结构 + 反编译
import struct, sys, os
sys.path.insert(0, r'C:\Users\20751\Desktop\猫和老鼠')

b = open(r'C:\Users\20751\tomdump\live_segs\x1_enc.bin', 'rb').read()

def rd_tstr(buf, pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

def parse_end(buf, pos):
    """解析函数结构, 返回结束位置"""
    try:
        ln = struct.unpack_from('<I', buf, pos)[0]
        if ln > 0x100000: return None
        src, pos = rd_tstr(buf, pos)
        pos += 12
        sc = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if sc > 0x400000: return None
        pos += sc * 4
        sizek = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        for _ in range(sizek):
            t = buf[pos]; pos += 1
            if t == 0: pass
            elif t == 1: pos += 1
            elif t == 3: pos += 8
            elif t == 4:
                _, pos = rd_tstr(buf, pos)
            else: return None
        sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        for _ in range(sizep):
            e = parse_end(buf, pos)
            if e is None: return None
            pos = e
        for field in range(3):
            n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
            if n > 0x1000000: return None
            if field == 0: pos += n * 4
            elif field == 1:
                for _ in range(n):
                    _, pos = rd_tstr(buf, pos)
                    pos += 8
            else:
                for _ in range(n):
                    _, pos = rd_tstr(buf, pos)
        return pos
    except Exception:
        return None

for start, name in [(0x1f898, 'BattleHotfixSystem'), (0xe1348, 'BaseReader'), (0x100bb8, 'RoleSpineAsync')]:
    end = parse_end(b, start)
    if end is None:
        print(f'{name}: 解析失败 @{hex(start)}')
        continue
    sz = end - start
    print(f'{name}: @{hex(start)} 大小 {sz}B (0x{sz:x})')
    # 保存 + 加头
    out = b'\x1bLuaQ\x00\x01\x04\x04\x04\x08\x00' + b[start:end]
    fn = rf'C:\Users\20751\tomdump\live_segs\{name}.luac'
    open(fn, 'wb').write(out)
    print(f'  已存 {fn}')
