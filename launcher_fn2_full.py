# -*- coding: utf-8 -*-
# fn#2 完整反编译 (用 vm_pseudo_gen 的正确映射)
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()

NAMES = {
    0: 'SETTABLE', 1: 'OP1', 2: 'OP2', 3: 'LOADBOOL',
    4: 'CALL', 5: 'RETURN', 6: 'FORLOOP', 7: 'MOVE',
    8: 'FORPREP', 9: 'CALLSETUP', 10: 'LOADIMM', 11: 'OP11',
    12: 'OP12', 13: 'OP13', 14: 'TEST', 15: 'OP15',
    16: 'OP16', 17: 'GETTABLE', 18: 'CONCAT', 19: 'OP19',
    20: 'LOADK', 21: 'JMP', 22: 'EQ', 23: 'OP23',
    24: 'OP24', 25: 'GETTABLE2', 26: 'OP26', 27: 'OP27',
    28: 'LOOPEND', 29: 'OP29', 30: 'NEWTABLE', 31: 'OP31',
    32: 'OP32', 33: 'SELF', 34: 'GETGLOBAL', 35: 'ARITH', 36: 'SETTABLEK', 37: 'OP37',
    38: 'OP38', 39: 'OP39', 40: 'OP40', 41: 'OP41',
}

def rd_tstr(pos):
    if pos + 4 > len(buf): return None, pos
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0 or ln > 0x100000: return b'', pos + 4
    if pos + 4 + ln > len(buf): return None, pos
    return buf[pos+4:pos+4+ln-1], pos + 4 + ln

def get_fn2():
    r = rd_tstr(12)
    pos = r[1] + 12
    sc = struct.unpack_from('<I', buf, pos)[0]
    pos += 4 + sc * 4
    sizek = struct.unpack_from('<I', buf, pos)[0]
    pos += 4
    for i in range(sizek):
        t = buf[pos]; pos += 1
        if t == 0: pass
        elif t == 1: pos += 1
        elif t == 3: pos += 8
        elif t == 4:
            rr = rd_tstr(pos); pos = rr[1]
    sizep = struct.unpack_from('<I', buf, pos)[0]
    pos += 4
    # 跳过 fn#0, fn#1, 到 fn#2
    for fi in range(2):
        # 解析一个子函数 (用容错 walk)
        def walk(p):
            r = rd_tstr(p)
            _, p = r
            p += 12
            sc2 = struct.unpack_from('<I', buf, p)[0]
            p += 4 + sc2 * 4
            sizek2 = struct.unpack_from('<I', buf, p)[0]
            p += 4
            for i in range(sizek2):
                t = buf[p]; p += 1
                if t == 0: pass
                elif t == 1: p += 1
                elif t == 3: p += 8
                elif t == 4:
                    rr = rd_tstr(p); p = rr[1]
            sizep2 = struct.unpack_from('<I', buf, p)[0]
            p += 4
            for i in range(sizep2):
                p = walk(p)
            n = struct.unpack_from('<I', buf, p)[0]; p += 4
            p += n * 4
            n = struct.unpack_from('<I', buf, p)[0]; p += 4
            for _ in range(n):
                rr = rd_tstr(p); _, p = rr
                p += 8
            n = struct.unpack_from('<I', buf, p)[0]; p += 4
            for _ in range(n):
                rr = rd_tstr(p); _, p = rr
            return p
        pos = walk(pos)
    # 现在 pos 指向 fn#2
    r = rd_tstr(pos)
    _, p = r
    p += 12
    sc2 = struct.unpack_from('<I', buf, p)[0]
    code = struct.unpack_from('<%dI' % sc2, buf, p + 4)
    p += 4 + sc2 * 4
    sizek2 = struct.unpack_from('<I', buf, p)[0]
    p += 4
    ks = []
    for i in range(sizek2):
        t = buf[p]; p += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(bool(buf[p])); p += 1
        elif t == 3: ks.append(struct.unpack_from('<d', buf, p)[0]); p += 8
        elif t == 4:
            rr = rd_tstr(p); ks.append(rr[0]); p = rr[1]
    return code, ks

code, ks = get_fn2()
print('fn#2 sc=%d k=%d' % (len(code), len(ks)))
print()
for i, ins in enumerate(code):
    op = ins & 0x3F
    A = (ins >> 6) & 0xFF
    B = (ins >> 14) & 0x1FF
    C = (ins >> 23) & 0x1FF
    Bx = (ins >> 14) & 0x3FFFF
    nm = NAMES.get(op, 'OP%d' % op)
    extra = ''
    if nm in ('LOADK', 'GETGLOBAL', 'SETTABLEK') and Bx < len(ks) and ks[Bx]:
        extra = ' [%r]' % (ks[Bx],)
    print('  %5d %-10s A=%d B=%d C=%d Bx=%d%s' % (i, nm, A, B, C, Bx, extra))
