# -*- coding: utf-8 -*-
# 分步解析 launcher 主函数, 定位解析断点
import struct

buf = open(r'C:\Users\20751\tomdump\dd_live_1973\s631.bin', 'rb').read()
LIMIT = len(buf)
p = 0x754
out = []
lines = []

def rd_tstr(pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln > 0x100000: raise ValueError(f'tstr len {ln} @{pos:#x}')
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

def parse_proto(pos, depth):
    global out
    ln = struct.unpack_from('<I', buf, pos)[0]
    src, pos = rd_tstr(pos)
    ld = struct.unpack_from('<i', buf, pos)[0]; pos += 4
    lld = struct.unpack_from('<i', buf, pos)[0]; pos += 4
    nups = buf[pos]; numparams = buf[pos+1]; isvar = buf[pos+2]; maxst = buf[pos+3]; pos += 4
    sc = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    print(f'{"  "*depth}proto @{pos-4-4-4-4-sc*0:#x} src={src!r} ld={ld} lld={lld} nups={nups} np={numparams} va={isvar} ms={maxst} sizecode={sc}', flush=True)
    if not (0 <= sc <= 0x1000000): raise ValueError(f'sizecode {sc}')
    code = struct.unpack_from('<%dI' % sc, buf, pos)
    pos += sc * 4
    # 常量
    sizek = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    if sizek > 0x100000: raise ValueError('sizek')
    ks = []
    for i in range(sizek):
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(buf[pos] != 0); pos += 1
        elif t == 3: ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            s, pos = rd_tstr(pos); ks.append(s)
        else:
            raise ValueError(f'const type {t} @{pos-1:#x} i={i}')
    print(f'{"  "*depth}  sizek={sizek} 前几个: {ks[:6]}', flush=True)
    # 子函数
    sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    if sizep > 0x100000: raise ValueError('sizep')
    print(f'{"  "*depth}  sizep={sizep}', flush=True)
    for i in range(sizep):
        pos = parse_proto(pos, depth + 1)
    # 调试段
    for field, nm in [(0,'lineinfo'),(1,'locvars'),(2,'upvalues')]:
        n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if n > 0x1000000: raise ValueError(f'{nm} n={n}')
        if nm == 'lineinfo': pos += n * 4
        elif nm == 'locvars':
            for _ in range(n):
                s, pos = rd_tstr(pos)
                pos += 8
        else:
            for _ in range(n):
                s, pos = rd_tstr(pos)
    return pos

try:
    end = parse_proto(0x754, 0)
    print(f'✓ 完整解析到 0x{end:x} (段内偏移 0x{end-0x748:x})')
except ValueError as e:
    print(f'✗ 失败: {e} @ 偏移 0x{p-0x748:x} (段内)')
