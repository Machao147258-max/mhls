# -*- coding: utf-8 -*-
# Lua 伪代码生成器 (基于确认的 opcode 语义)
# 把指令流翻译成可读的 Lua 伪代码 (栈寄存器模型)
import struct, sys, re

SO = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so','rb').read()
FMT = SO[0xcd3820:0xcd3820+42]

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

def parse_file(path):
    b = open(path, 'rb').read()
    out = []
    pos = 12
    def parse_proto(pos, depth):
        if pos + 4 > len(b): return None
        ln = struct.unpack_from('<I', b, pos)[0]
        if ln > 0x100000: return None
        src = b[pos+4:pos+4+ln-1]
        pos += 4 + ln
        if pos + 16 > len(b): return None
        pos += 12
        sc = struct.unpack_from('<I', b, pos)[0]
        if sc > 0x1000000: return None
        pos += 4
        code = struct.unpack_from('<%dI' % sc, b, pos)
        pos += sc * 4
        if pos + 4 > len(b): return None
        sizek = struct.unpack_from('<I', b, pos)[0]
        if sizek > 0x100000: return None
        pos += 4
        ks = []
        for _ in range(sizek):
            if pos >= len(b): return None
            t = b[pos]; pos += 1
            if t == 0: ks.append(None)
            elif t == 1: ks.append(bool(b[pos])); pos += 1
            elif t == 3: ks.append(struct.unpack_from('<d', b, pos)[0]); pos += 8
            elif t == 4:
                l2 = struct.unpack_from('<I', b, pos)[0]
                if l2 > 0x100000: return None
                ks.append(b[pos+4:pos+4+l2-1].decode('utf-8','replace'))
                pos += 4 + l2
            elif t == 2:
                ks.append('<userdata>'); pos += 8
            else:
                # 未知类型/截断: 停止常量解析 (内存格式差异)
                break
        # 子函数 (容错: 常量区异常时跳过)
        if pos + 4 > len(b):
            return None
        sizep = struct.unpack_from('<I', b, pos)[0]
        if sizep <= 0x100000 and sizep <= (len(b) - pos) // 16:
            pos += 4
            for _ in range(sizep):
                r = parse_proto(pos, depth+1)
                if r is None: return None
                pos = r
            for field in range(3):
                if pos + 4 > len(b): return None
                n = struct.unpack_from('<I', b, pos)[0]
                if n > 0x1000000: return None
                pos += 4
                if field == 0: pos += n * 4
                elif field == 1:
                    for _ in range(n):
                        if pos + 4 > len(b): return None
                        l2 = struct.unpack_from('<I', b, pos)[0]; pos += 4
                        if l2 > 0x100000: return None
                        pos += l2 + 8
                else:
                    for _ in range(n):
                        if pos + 4 > len(b): return None
                        l2 = struct.unpack_from('<I', b, pos)[0]; pos += 4
                        if l2 > 0x100000: return None
                        pos += l2
        # 生成伪代码
        ind = '  ' * depth
        sname = src.decode('utf-8', 'replace') if src else '<anon>'
        out.append(f'{ind}function {sname}()')
        ks_str = {i: repr(k)[:40] for i, k in enumerate(ks)}
        # 跳转目标表
        targets = {}
        for j, v in enumerate(code):
            op = v & 0x3F
            mode = FMT[op] & 3 if op < 42 else 0
            if mode == 2:
                bx = (v >> 14) & 0x3FFFF
                t = j + 1 + (bx - 131071)
                targets.setdefault(t, []).append(j)
        for j, v in enumerate(code):
            op = v & 0x3F
            a = (v >> 6) & 0xFF
            b2 = (v >> 14) & 0x1FF
            c = (v >> 23) & 0x1FF
            bx = (v >> 14) & 0x3FFFF
            mode = FMT[op] & 3 if op < 42 else 0
            name = NAMES.get(op, f'OP{op}')
            lbl = f'  {ind}-- L{j}' if j in targets else ''
            if lbl: out.append(lbl)
            line = f'{ind}  [{j:3d}] {name}'
            def K(x):  # 常量显示
                if x is None: return 'nil'
                if isinstance(x, bool): return 'true' if x else 'false'
                if isinstance(x, float): return f'{x:g}'
                return f'\"{x}\"'
            if mode == 1:
                line += f' R{a} <- K{bx}' if 0 <= bx < len(ks) else f' R{a} <- imm{bx}'
            elif mode == 2:
                line += f' (pc+{bx-131071})'
            else:
                def KV(x):
                    # 常量索引 (256+) → 值
                    if x >= 256 and x - 256 < len(ks):
                        return f'K{x}({K(ks[x-256])})'
                    return f'R{x}'
                bb = KV(b2) if b2 >= 256 else f'R{b2}'
                cc = KV(c) if c >= 256 else f'R{c}'
                if op == 4: line += f' {bb}({cc})'
                elif op == 17 or op == 25: line += f' R{a} <- {cc}[{bb}]'
                elif op == 36: line += f' R{a}[{cc}] <- {bb}'
                elif op == 7: line += f' R{a} <- {cc}'
                elif op == 5: line += f' return R{a}({c-1})'
                elif op == 33: line += f' R{a} <- {cc}:method({bb})'
                elif op == 35: line += f' R{a} <- {bb} OP {cc}'
                elif op == 22: line += f' if {bb} == {cc}'
                elif op == 30: line += f' R{a} <- {{}}(size {b2})'
                elif op == 14: line += f' test R{a}'
                elif op == 3: line += f' R{a} <- bool({b2})'
                elif op == 0: line += f' {cc}[{bb}] <- ?'
                else: line += f' R{a}, {bb}, {cc}'
            if 0 <= bx-256 < len(ks) and (mode == 0 and op == 36):
                pass
            # 常量注释
            if mode == 1 and 0 <= bx < len(ks):
                line += f'  ; {K(ks[bx])}'
            out.append(line)
        out.append(f'{ind}end')
        return pos
    parse_proto(pos, 0)
    return out

if __name__ == '__main__':
    import os
    target = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\20751\tomdump\mega_luac\src_catchGame_systems_UGCSystem.lua.luac'
    lines = parse_file(target)
    base = os.path.splitext(target)[0]
    with open(base + '.lua_pseudo', 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    print(f'✓ {base}.lua_pseudo ({len(lines)} 行)')