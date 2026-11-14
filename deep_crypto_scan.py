# -*- coding: utf-8 -*-
# 完整反编译 (顶层+全部子函数) + 搜 Crypto/decrypt/key 调用
import struct, sys, os

sys.path.insert(0, r'C:\Users\20751\Desktop\猫和老鼠')
from vm_rev_decompiler import parse_proto, Decompiler, kstr

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

def walk_proto(p, depth=0, out=None):
    """递归所有子函数, 反汇编找关键调用"""
    consts = p['consts']
    code = p['code']
    # 顶层反编译
    d = Decompiler(p)
    try:
        src_text = d.run()
    except Exception:
        src_text = ''
    # 找 Crypto/decrypt/key 常量
    kws = []
    for c in consts:
        if isinstance(c, str):
            cl = c.lower()
            if any(k in cl for k in ['crypt', 'decrypt', 'encrypt', 'x1v5', 'getkey', 'setkey', 'teakey', 'golden']):
                kws.append(c)
    if kws:
        out.append(('  ' * depth) + f'[★KEYWORDS] {kws}')
    # 反汇编找 LOADK 这些常量 + CALL 模式
    for i, ins in enumerate(code):
        op = ins & 0x3F
        A = (ins >> 6) & 0xFF
        Bx = (ins >> 14) & 0x3FFFF
        if op == 20 and Bx < len(consts) and isinstance(consts[Bx], str):
            cl = consts[Bx].lower()
            if any(k in cl for k in ['crypt', 'decrypt', 'encrypt', 'x1v5', 'key']):
                out.append(('  ' * depth) + f'  [ins {i}] LOADK {consts[Bx]!r}')
                # 看前后
                for j in range(max(0, i-3), min(len(code), i+5)):
                    opj = code[j] & 0x3F
                    Aj = (code[j] >> 6) & 0xFF
                    Bxj = (code[j] >> 14) & 0x3FFFF
                    ext = ''
                    if opj == 20 and Bxj < len(consts) and consts[Bxj] is not None:
                        ext = ' %r' % (consts[Bxj],)
                    out.append(('  ' * (depth+1)) + f'[{j}] {NAMES.get(opj, "OP%d" % opj)} A={Aj} Bx={Bxj}{ext}')
                out.append('')
    for i, pr in enumerate(p['protos']):
        walk_proto(pr, depth + 1, out)

def full(path):
    b = open(path, 'rb').read()
    r = parse_proto(b)
    if r is None:
        print('解析失败')
        return
    ep, p = r
    out = []
    walk_proto(p, 0, out)
    return '\n'.join(out)

for f, name in [(r'C:\Users\20751\tomdump\harvest2\full_BaseReader.luac', 'BaseReader'),
                (r'C:\Users\20751\tomdump\harvest2\full_BattleHotfixSystem.luac', 'BattleHotfixSystem'),
                (r'C:\Users\20751\tomdump\harvest2\full_RoleSpineAsync.luac', 'RoleSpineAsync')]:
    txt = full(f)
    print(f'=== {name} ===')
    print(txt if txt else '(无关键调用)')
    print()
