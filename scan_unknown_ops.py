# -*- coding: utf-8 -*-
# 扫描未知 op 的上下文模式 (launcher 主函数 + fn#2), 从语义钉死
import struct, sys, re

sys.path.insert(0, r'C:\Users\20751\Desktop\猫和老鼠')
buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()
SO = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so','rb').read()
FMT = SO[0xcd3820:0xcd3820+42]
NAMES = {0:'LT',1:'LE',2:'TESTSET',3:'LOADBOOL',4:'CALL',5:'RETURN',6:'FORLOOP',7:'MOVE',8:'FORPREP',9:'CALLSETUP',10:'LOADIMM',11:'GETUPVAL',12:'SETGLOBAL',13:'CLOSE',14:'TEST',15:'TAILCALL',16:'LEN',17:'GETTABLE',18:'CONCAT',19:'ADD',20:'LOADK',21:'JMP',22:'EQ',23:'FORCOND',24:'SUB',25:'GETTABLE2',26:'SETUPVAL',27:'MUL',28:'LOADNIL',29:'NOT',30:'NEWTABLE',31:'LOADNIL2',32:'DIV',33:'SELF',34:'GETGLOBAL',35:'ARITH',36:'SETTABLEK',37:'VARARG'}

def rd_tstr(pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

def walk(pos, depth, idx, out):
    ln = struct.unpack_from('<I', buf, pos)[0]
    src, pos = rd_tstr(pos)
    pos += 12
    sc = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    code = struct.unpack_from('<%dI' % sc, buf, pos); pos += sc*4
    sizek = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    ks = []
    for _ in range(sizek):
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(bool(buf[pos])); pos += 1
        elif t == 3: ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            s, pos = rd_tstr(pos); ks.append(s)
        else: raise ValueError('const')
    out.append((idx, src, sc, code, ks, depth))
    sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for i in range(sizep):
        try:
            pos = walk(pos, depth+1, i, out)
        except Exception:
            return pos  # 堆打断, 停止下降
    return pos

fns = []
walk(12, 0, 0, fns)

def kk(ks, i):
    if 0 <= i < len(ks): return repr(ks[i])
    return f'k?{i}'

def fmt_ins(v, ks):
    op = v & 0x3F; a = (v >> 6) & 0xFF
    b2 = (v >> 14) & 0x1FF; c = (v >> 23) & 0x1FF
    bx = (v >> 14) & 0x3FFFF
    mode = FMT[op] & 3 if op < 42 else 0
    name = NAMES.get(op, f'op{op}')
    ann = ''
    if op in (17, 25, 33, 36, 22, 0, 1, 19, 24, 27, 32, 35, 2, 14):
        if b2 >= 256 and b2-256 < len(ks): ann += f' B=k{kk(ks,b2-256)}'
        if c >= 256 and c-256 < len(ks): ann += f' C=k{kk(ks,c-256)}'
    if op in (20, 34):
        ki = bx - 256 if op == 20 else bx
        if 0 <= ki < len(ks): ann += f' Bx=k{kk(ks,ki)}'
    if mode == 1: return f'{name:9s} A={a:3d} Bx={bx:5d}{ann}'
    if mode == 2: return f'{name:9s} A={a:3d} sBx={bx-131071:6d}{ann}'
    return f'{name:9s} A={a:3d} B={b2:3d} C={c:3d}{ann}'

TARGETS = {0, 1, 3, 11, 12, 13, 15, 16, 19, 24, 26, 27, 29, 32, 35, 37}
for idx, src, sc, code, ks, depth in fns:
    hits = [i for i, v in enumerate(code) if (v & 0x3F) in TARGETS]
    if not hits: continue
    print(f'\n===== fn#{idx} ({sc} instr) 未知op 命中 {len(hits)} ====')
    shown = {}
    for i in hits:
        op = code[i] & 0x3F
        shown[op] = shown.get(op, 0) + 1
        if shown[op] > 2: continue
        lo, hi = max(0, i-2), min(sc, i+3)
        for j in range(lo, hi):
            mark = '>>' if j == i else '  '
            print(f'{mark}[{j:3d}] {fmt_ins(code[j], ks)}')
        print('---')
