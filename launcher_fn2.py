# -*- coding: utf-8 -*-
# launcher fn#2 反汇编 (基于能跑通的 launcher_consts.py 结构)
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()

def rd_tstr(pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

results = {}
def walk(pos, depth, fidx):
    ln = struct.unpack_from('<I', buf, pos)[0]
    src, pos = rd_tstr(pos)
    pos += 12
    sc = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    code = struct.unpack_from('<%dI' % sc, buf, pos); pos += sc * 4
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
            raise ValueError('const %d' % t)
    sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for i in range(sizep):
        pos = walk(pos, depth+1, i)
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    pos += n * 4
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos); pos += 8
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos)
    if fidx == 2 and depth == 1:
        results['fn2'] = {'code': code, 'k': ks}
    return pos

try:
    walk(12, 0, 0)
    fn2 = results.get('fn2')
    if not fn2:
        print('未捕获 fn#2')
    else:
        code, k = fn2['code'], fn2['k']
        print('fn#2: sc=%d k=%d' % (len(code), len(k)))
        for i, kk in enumerate(k):
            print('  k[%d] = %r' % (i, kk))
        print()
        OPS = {34: 'LOADK', 20: 'GETGLOBAL'}
        for i, ins in enumerate(code):
            op = ins & 0x3F
            A = (ins >> 6) & 0xFF
            B = (ins >> 14) & 0x1FF
            C = (ins >> 23) & 0x1FF
            Bx = (ins >> 14) & 0x3FFFF
            nm = OPS.get(op, 'OP%d' % op)
            extra = ''
            if nm == 'LOADK' and Bx < len(k):
                extra = ' k[%d]=%r' % (Bx, k[Bx])
            if nm == 'GETGLOBAL' and Bx < len(k):
                extra = ' g[%d]=%r' % (Bx, k[Bx])
            print('  %5d %-10s A=%d B=%d C=%d Bx=%d%s' % (i, nm, A, B, C, Bx, extra))
except Exception as e:
    import traceback
    traceback.print_exc()
