# -*- coding: utf-8 -*-
# 表构造还原: 把纯数据脚本 (LOADK+SETTABLEK+NEWTABLE) 反编译为 Lua 表字面量
# 输入: luac 二进制 → 输出: 可读的 Lua 表构造代码
import struct, sys, re, os

def parse_proto(b, pos=12, depth=0):
    """解析 Lua 5.1 prototype, 返回 (end_pos, proto_dict)"""
    if pos + 4 > len(b): return None
    src_len = struct.unpack_from('<I', b, pos)[0]
    if src_len > 0x100000: return None
    pos += 4 + src_len
    pos += 12  # linedefined, lastlinedefined, numparams+is_vararg+maxstacksize (4B)
    if pos + 4 > len(b): return None
    sc = struct.unpack_from('<I', b, pos)[0]
    if sc > 0x1000000: return None
    pos += 4
    code = list(struct.unpack_from('<%dI' % sc, b, pos)) if sc > 0 else []
    pos += sc * 4
    if pos + 4 > len(b): return None
    sizek = struct.unpack_from('<I', b, pos)[0]
    pos += 4
    consts = []
    for _ in range(sizek):
        if pos >= len(b): return None
        t = b[pos]; pos += 1
        if t == 0:
            consts.append(None)
        elif t == 1:
            consts.append(bool(b[pos])); pos += 1
        elif t == 3:
            consts.append(struct.unpack_from('<d', b, pos)[0]); pos += 8
        elif t == 4:
            l = struct.unpack_from('<I', b, pos)[0]
            if l > 0x100000: return None
            pos += 4
            consts.append(b[pos:pos+l].decode('utf-8', 'replace'))
            pos += l
        else:
            return None
    if pos + 4 > len(b): return None
    sizep = struct.unpack_from('<I', b, pos)[0]
    pos += 4
    protos = []
    for _ in range(sizep):
        r = parse_proto(b, pos, depth + 1)
        if r is None: return None
        ep, p = r
        protos.append(p)
        pos = ep
    # debug 段跳过
    for field in range(3):
        if pos + 4 > len(b): return None
        n = struct.unpack_from('<I', b, pos)[0]
        if n > 0x1000000: return None
        pos += 4
        if field == 0:
            pos += n * 4
        elif field == 1:
            for _ in range(n):
                if pos + 4 > len(b): return None
                l = struct.unpack_from('<I', b, pos)[0]; pos += 4
                if l > 0x100000: return None
                pos += l + 8
        else:
            for _ in range(n):
                if pos + 4 > len(b): return None
                l = struct.unpack_from('<I', b, pos)[0]; pos += 4
                if l > 0x100000: return None
                pos += l
    return (pos, {'code': code, 'consts': consts, 'protos': protos, 'src_len': src_len})

# opcode 语义 (已确认)
NAME = {4: 'CALL', 5: 'RETURN', 7: 'MOVE', 9: 'CALLSETUP', 10: 'LOADIMM', 14: 'TEST',
        17: 'GETTABLE', 20: 'LOADK', 21: 'JMP', 22: 'EQ', 25: 'GETTABLE2', 28: 'LOOPEND?',
        30: 'NEWTABLE', 33: 'SELF', 34: 'GETGLOBAL', 35: 'ARITH', 36: 'SETTABLEK', 3: 'LOADBOOL',
        4: 'CALL', 0: 'LT?', 1: 'LE?', 2: 'TESTSET', 5: 'RETURN', 6: 'FORLOOP?', 8: 'FORPREP?',
        11: 'GETUPVAL?', 12: 'SETGLOBAL?', 13: 'CLOSE?', 15: 'TAILCALL?', 16: 'LEN?',
        18: 'CONCAT?', 19: 'ADD?', 23: 'FORCOND?', 24: 'SUB?', 26: 'SETUPVAL?', 27: 'MUL?',
        29: 'NOT?', 31: 'LOADNIL2?', 32: 'DIV?', 37: 'VARARG?', 38: 'SPECIAL?', 39: 'SPECIAL?',
        40: 'SPECIAL?', 41: 'SPECIAL?'}

def fmt_const(c):
    if c is None: return 'nil'
    if isinstance(c, bool): return 'true' if c else 'false'
    if isinstance(c, float):
        return repr(int(c)) if c == int(c) else repr(c)
    if isinstance(c, str):
        # 剥尾部 \x00 (引擎字符串填充)
        s = c.rstrip('\x00')
        return repr(s)
    return repr(c)

def fmt_code(code, consts):
    """指令 → 行"""
    lines = []
    for i, v in enumerate(code):
        op = v & 0x3F
        a = (v >> 6) & 0xFF
        c = (v >> 14) & 0x1FF
        b = (v >> 23) & 0x1FF
        Bx = (v >> 14) & 0x3FFFF
        sBx = Bx - 131071
        name = NAME.get(op, f'OP{op}')
        if op == 20:  # LOADK
            lines.append((i, f'{name} R{a} = K{Bx} {fmt_const(consts[Bx]) if Bx < len(consts) else "?"}'))
        elif op == 36:  # SETTABLEK
            bb = b if b < 256 else f'K{b-256}'
            lines.append((i, f'{name} R{a}[K{c}] = R{bb}'))
        elif op == 30:  # NEWTABLE
            lines.append((i, f'{name} R{a} (array={c+1}, hash={b+1})'))
        elif op == 17:  # GETTABLE
            lines.append((i, f'{name} R{a} = R{b}[R{c}]'))
        else:
            lines.append((i, f'{name} A={a} B={b} C={c} Bx={Bx}'))
    return lines

def gen_table(code, consts):
    """尝试把 SETTABLEK 序列还原为表字面量"""
    # 先做寄存器值跟踪: LOADK R[a] = K[Bx] → reg_val[a] = 常量
    reg_val = {}
    for v in code:
        op = v & 0x3F
        if op == 20:  # LOADK
            a = (v >> 6) & 0xFF
            Bx = (v >> 14) & 0x3FFFF
            reg_val[a] = consts[Bx] if Bx < len(consts) else None
    def rval(b):
        if b < 256:
            if b in reg_val:
                return fmt_const(reg_val[b])
            return f'<R{b}>'
        return fmt_const(consts[b - 256]) if b - 256 < len(consts) else f'<K{b-256}>'
    out = []
    i = 0
    n = len(code)
    while i < n:
        v = code[i]
        op = v & 0x3F
        if op == 30:  # NEWTABLE
            a = (v >> 6) & 0xFF
            entries = []
            j = i + 1
            # 收集后续 SETTABLEK(同一 R[a])
            while j < n:
                w = code[j]
                wop = w & 0x3F
                wa = (w >> 6) & 0xFF
                if wop == 36 and wa == a:
                    ck = (w >> 14) & 0x1FF
                    bk = (w >> 23) & 0x1FF
                    key = fmt_const(consts[ck]) if ck < len(consts) else '?'
                    val = rval(bk)
                    entries.append((key, val))
                    j += 1
                elif wop == 30 or (wop == 20 and wa != a and entries):
                    break
                elif wop == 5:  # RETURN
                    break
                else:
                    j += 1
            if entries:
                t = '{\n' + '\n'.join(f'    [{k}] = {v},' for k, v in entries) + '\n  }'
                out.append((i, f'R{a} = {t} (NEWTABLE)'))
                i = j
                continue
        out.append((i, None))
        i += 1
    return out

def main(fn):
    b = open(fn, 'rb').read()
    if not b.startswith(b'\x1bLuaQ'):
        print('不是 luac!'); return
    r = parse_proto(b)
    if r is None:
        print('解析失败'); return
    _, p = r
    print(f'// 文件: {os.path.basename(fn)}')
    print(f'// 顶层原型: code={len(p["code"])} consts={len(p["consts"])} protos={len(p["protos"])}')
    print()
    # 顶层: 全表还原
    lines = gen_table(p['code'], p['consts'])
    for i, l in lines:
        if l:
            print(l)
        else:
            v = p['code'][i]
            op = v & 0x3F
            print(f'// [{i}] {NAME.get(op, f"OP{op}")} A={(v>>6)&0xFF} B={(v>>23)&0x1FF} C={(v>>14)&0x1FF}')
    print()
    # 统计
    from collections import Counter
    ops = Counter((v & 0x3F) for v in p['code'])
    print(f'// opcode 分布: {dict(sorted(ops.items()))}')

if __name__ == '__main__':
    main(sys.argv[1])