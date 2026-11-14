# -*- coding: utf-8 -*-
# 容错解析 launcher_raw.luac → fn#2 (加密子函数) 指令
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()

def rd_tstr(pos):
    if pos + 4 > len(buf): return None, pos
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0 or ln > 0x100000: return b'', pos + 4
    if pos + 4 + ln > len(buf): return None, pos
    return buf[pos+4:pos+4+ln-1], pos + 4 + ln

def walk(pos, depth, fidx, found):
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
            r = rd_tstr(pos)
            if r[0] is None: ok = False; break
            ks.append(r[0]); pos = r[1]
        else:
            ok = False; break
    if not ok: return None
    if pos + 4 > len(buf): return None
    sizep = struct.unpack_from('<I', buf, pos)[0]
    if sizep > 0x100000: return None
    pos += 4
    protos = []
    for i in range(sizep):
        r = walk(pos, depth+1, i, found)
        if r is None: return None
        pos = r
    # debug 段 (容错)
    try:
        n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if n > 0x1000000: return None
        pos += n * 4
        n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if n > 0x100000: return None
        for _ in range(n):
            r = rd_tstr(pos)
            if r[0] is None: return None
            _, pos = r
            pos += 8
        n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        if n > 0x100000: return None
        for _ in range(n):
            r = rd_tstr(pos)
            if r[0] is None: return None
            _, pos = r
    except Exception:
        return None
    if fidx == 2 and depth == 1:
        found['fn2'] = {'code': None, 'k': ks, 'sc': sc}
        # 重读 code
        found['code_off'] = None
    return pos

# 手动: 解析主函数拿 protos 偏移, 逐个子函数容错
def get_main():
    r = rd_tstr(12)
    if r[0] is None: return None
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
            r = rd_tstr(pos); pos = r[1]
        else:
            return None
    sizep = struct.unpack_from('<I', buf, pos)[0]
    pos += 4
    return pos, sizep

try:
    m = get_main()
    if not m:
        print('主函数解析失败')
    else:
        pos, sizep = m
        print('主函数 protos 区 @ %#x, %d 个子函数' % (pos, sizep))
        for i in range(sizep):
            start = pos
            r = walk(pos, 1, i, {})
            if r is None:
                print('fn#%d @ %#x: 解析失败' % (i, start))
                break
            pos = r
            print('fn#%d @ %#x: OK' % (i, start))
        # fn#2 单独反汇编
        found = {}
        pos2, _ = m
        for i in range(2):
            pos2 = walk(pos2, 1, i, {})
        # 重新解析 fn#2 拿指令
        r = rd_tstr(pos2)
        _, p2 = r
        p2 += 12
        sc2 = struct.unpack_from('<I', buf, p2)[0]
        code2 = struct.unpack_from('<%dI' % sc2, buf, p2 + 4)
        print()
        print('=== fn#2 sc=%d ===' % sc2)
        OPS = {34: 'LOADK', 20: 'GETGLOBAL'}
        # 需要常量 —— 从 walk 结果再取 (简化: 重解析一次)
        r = rd_tstr(pos2)
        _, p3 = r
        p3 += 12
        sc3 = struct.unpack_from('<I', buf, p3)[0]
        p3 += 4 + sc3 * 4
        sizek3 = struct.unpack_from('<I', buf, p3)[0]
        p3 += 4
        ks = []
        for i in range(sizek3):
            t = buf[p3]; p3 += 1
            if t == 0: ks.append(None)
            elif t == 1: ks.append(bool(buf[p3])); p3 += 1
            elif t == 3: ks.append(struct.unpack_from('<d', buf, p3)[0]); p3 += 8
            elif t == 4:
                rr = rd_tstr(p3); ks.append(rr[0]); p3 = rr[1]
        for i, kk in enumerate(ks):
            print('  k[%d] = %r' % (i, kk))
        print()
        for i, ins in enumerate(code2):
            op = ins & 0x3F
            A = (ins >> 6) & 0xFF
            B = (ins >> 14) & 0x1FF
            C = (ins >> 23) & 0x1FF
            Bx = (ins >> 14) & 0x3FFFF
            nm = OPS.get(op, 'OP%d' % op)
            extra = ''
            if nm == 'LOADK' and Bx < len(ks):
                extra = ' k[%d]=%r' % (Bx, ks[Bx])
            if nm == 'GETGLOBAL' and Bx < len(ks):
                extra = ' g[%d]=%r' % (Bx, ks[Bx])
            print('  %5d %-10s A=%d B=%d C=%d Bx=%d%s' % (i, nm, A, B, C, Bx, extra))
except Exception as e:
    import traceback
    traceback.print_exc()
