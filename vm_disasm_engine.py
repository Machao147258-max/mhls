# -*- coding: utf-8 -*-
# 正式反汇编工具: 猫和老鼠(tom)魔改 VM
# 用法: python disasm_engine.py <luac文件> [输出文件]
# 已确认 opcode: 4=CALL 17=GETTABLE 20=LOADK 30=RETURN 33=SELF 34=GETGLOBAL 36=LOADK2(双常量)
import struct, sys, os, glob

SO = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so','rb').read()
FMT = SO[0xcd3820:0xcd3820+42]

NAMES = {
    0: 'LT?', 1: 'LE?', 2: 'TESTSET', 3: 'LOADBOOL',
    4: 'CALL', 5: 'RETURN', 6: 'FORLOOP?', 7: 'MOVE',
    8: 'FORPREP?', 9: 'CALLSETUP', 10: 'LOADIMM', 11: 'GETUPVAL?',
    12: 'SETGLOBAL', 13: 'CLOSE?', 14: 'TEST', 15: 'TAILCALL?',
    16: 'CONCAT2', 17: 'GETTABLE', 18: 'CONCAT?', 19: 'ADD?',
    20: 'LOADK', 21: 'JMP', 22: 'EQ', 23: 'FORCOND?',
    24: 'SUB?', 25: 'GETTABLE2', 26: 'SETUPVAL?', 27: 'MUL?',
    28: 'LOADNIL?', 29: 'NOT?', 30: 'NEWTABLE', 31: 'LOADNIL2?',
    32: 'DIV?', 33: 'SELF', 34: 'GETGLOBAL', 35: 'ARITH', 36: 'SETTABLEK', 37: 'VARARG?',
    38: 'SPECIAL?', 39: 'SPECIAL?', 40: 'SPECIAL?', 41: 'SPECIAL?',
}

# 本会话实证确认 (2026-08-11, 证据: launcher_raw.luac):
#   op0  LT: R[B] < R[C] (B/C 常量感知 256+k), A=0 → 条件真跳
#   op12 SETGLOBAL: global[k[Bx]] = R[A]  (Bx 直接常量索引)
#   op16 CONCAT2: R[A] = R[C] .. R[B]  (二元字符串拼接, B/C 均为寄存器, 常量先 LOADK)
#   op7  MOVE: R[A] = R[C]  (B 恒 0! 本 VM "C 中心")
#   op17 GETTABLE: R[A] = R[C][B]  (B=键 256+k 或寄存器, C=表)
#   op4  CALL: fn=R[A], nargs=B+1, 结果数=C-1 (C=0 → 多返回)
#   op20/34/12: Bx 直接常量索引 (无 -256)

def parse_proto(b, pos, depth=0, out=None):
    """解析一个函数块, 返回 (结束位置, 信息)"""
    if pos + 4 > len(b): return None, None
    ln = struct.unpack_from('<I', b, pos)[0]
    if ln > 0x100000: return None, None
    pos += 4
    src = b[pos:pos+ln-1] if ln else b''
    pos += ln
    if pos + 16 > len(b): return None, None
    pos += 12
    sc = struct.unpack_from('<I', b, pos)[0]
    if sc > 0x1000000: return None, None
    pos += 4
    code = struct.unpack_from('<%dI' % sc, b, pos) if sc else ()
    pos += sc * 4
    if pos + 4 > len(b): return None, None
    sizek = struct.unpack_from('<I', b, pos)[0]
    if sizek > 0x100000: return None, None
    pos += 4
    ks = []
    for _ in range(sizek):
        if pos >= len(b): return None, None
        t = b[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(bool(b[pos])); pos += 1
        elif t == 3: ks.append(struct.unpack_from('<d', b, pos)[0]); pos += 8
        elif t == 4:
            l2 = struct.unpack_from('<I', b, pos)[0]; pos += 4
            if l2 > 0x100000: return None, None
            ks.append(b[pos:pos+l2-1].decode('utf-8', 'replace') if l2 else '')
            pos += l2
        else:
            ks.append(f'<t{t}>'); pos += 1; break
    # 输出
    if out is not None:
        out.append('  ' * depth + f'--- 函数 {src!r} ({sc} 指令, {sizek} 常量) ---')
        for j, v in enumerate(code):
            op = v & 0x3F; a = (v >> 6) & 0xFF
            b2 = (v >> 14) & 0x1FF; c = (v >> 23) & 0x1FF
            bx = (v >> 14) & 0x3FFFF; sbx = bx - 131071
            mode = FMT[op] & 3 if op < 42 else 0
            name = NAMES.get(op, f'op{op}')
            if mode == 1:
                kt = f'  ; k[{bx-256}]={ks[bx-256]!r}' if 0 <= bx-256 < len(ks) else ''
                line = f'{name:9s} A={a:3d} Bx={bx:5d}{kt}'
            elif mode == 2:
                line = f'{name:9s} A={a:3d} sBx={sbx:6d}'
            else:
                line = f'{name:9s} A={a:3d} B={b2:3d} C={c:3d}'
                if op == 36 and 0 <= bx-256 < len(ks) and 0 <= c-256 < len(ks):
                    line += f'  ; k[{bx-256}]={ks[bx-256]!r} k[{c-256}]={ks[c-256]!r}'
            out.append('  ' * depth + f'[{j:3d}] {v:08x} {line}')
    # 子函数 (标准 sizep; 本格式下通常 0, 常量里可能有 Closure)
    if pos + 4 > len(b): return None, None
    sizep = struct.unpack_from('<I', b, pos)[0]
    if sizep > 0x100000: return None, None
    pos += 4
    for _ in range(sizep):
        r = parse_proto(b, pos, depth+1, out)
        if r[0] is None: return None, None
        pos = r[0]
    # 调试段
    for field in range(3):
        if pos + 4 > len(b): return None, None
        n = struct.unpack_from('<I', b, pos)[0]
        if n > 0x1000000: return None, None
        pos += 4
        if field == 0: pos += n * 4
        elif field == 1:
            for _ in range(n):
                if pos + 4 > len(b): return None, None
                l2 = struct.unpack_from('<I', b, pos)[0]; pos += 4
                if l2 > 0x100000: return None, None
                pos += l2 + 8
        else:
            for _ in range(n):
                if pos + 4 > len(b): return None, None
                l2 = struct.unpack_from('<I', b, pos)[0]; pos += 4
                if l2 > 0x100000: return None, None
                pos += l2
    return pos, {'src': src, 'code': sc, 'k': sizek}

def disasm_file(path):
    b = open(path, 'rb').read()
    out = []
    pos = 12
    r = parse_proto(b, pos, 0, out)
    return out

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print('用法: python disasm_engine.py <luac 文件或目录>')
        sys.exit(1)
    target = sys.argv[1]
    files = []
    if os.path.isdir(target):
        files = sorted(glob.glob(os.path.join(target, '*.luac')))
    else:
        files = [target]
    for f in files:
        try:
            lines = disasm_file(f)
            base = os.path.splitext(f)[0]
            with open(base + '.asm', 'w', encoding='utf-8') as fo:
                fo.write('\n'.join(lines))
            print(f'✓ {f} → {base}.asm ({len(lines)} 行)')
        except Exception as e:
            print(f'✗ {f}: {e}')