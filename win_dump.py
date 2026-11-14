# -*- coding: utf-8 -*-
# launcher 主函数指令窗口反汇编 (带常量注解) — 确认 LEN/LOADIMM 语义
import struct
buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()
SO = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so','rb').read()
FMT = SO[0xcd3820:0xcd3820+42]
NAMES = {0:'LT',1:'LE',2:'TESTSET',3:'LOADBOOL',4:'CALL',5:'RETURN',6:'FORLOOP',7:'MOVE',8:'FORPREP',9:'CALLSETUP',10:'LOADIMM',11:'GETUPVAL',12:'SETGLOBAL',13:'CLOSE',14:'TEST',15:'TAILCALL',16:'LEN',17:'GETTABLE',18:'CONCAT',19:'ADD',20:'LOADK',21:'JMP',22:'EQ',23:'FORCOND',24:'SUB',25:'GETTABLE2',26:'SETUPVAL',27:'MUL',28:'LOADNIL',29:'NOT',30:'NEWTABLE',31:'LOADNIL2',32:'DIV',33:'SELF',34:'GETGLOBAL',35:'ARITH',36:'SETTABLEK',37:'VARARG'}

p = 12
ln = struct.unpack_from('<I', buf, p)[0]; p += 4 + ln
p += 12
sc = struct.unpack_from('<I', buf, p)[0]; p += 4
code = struct.unpack_from('<%dI' % sc, buf, p)
p += sc * 4
sizek = struct.unpack_from('<I', buf, p)[0]; p += 4
ks = []
for _ in range(sizek):
    t = buf[p]; p += 1
    if t == 0: ks.append(None)
    elif t == 1: ks.append(bool(buf[p])); p += 1
    elif t == 3: ks.append(struct.unpack_from('<d', buf, p)[0]); p += 8
    elif t == 4:
        l = struct.unpack_from('<I', buf, p)[0]; p += 4
        ks.append(buf[p:p+l-1].decode('utf-8', 'replace') if l else '')
        p += l

def ann(v):
    op = v & 0x3F; a = (v >> 6) & 0xFF
    b2 = (v >> 14) & 0x1FF; c = (v >> 23) & 0x1FF
    bx = (v >> 14) & 0x3FFFF
    mode = FMT[op] & 3 if op < 42 else 0
    name = NAMES.get(op, f'op{op}')
    s = f'{name:9s} A={a:3d}'
    if mode == 2:
        s += f' sBx={bx-131071:5d}'
    elif mode == 1:
        ki = bx - 256 if op == 20 else bx
        s += f' Bx={bx:5d}'
        if 0 <= ki < len(ks): s += f'  k={ks[ki]!r}'
    else:
        s += f' B={b2:3d} C={c:3d}'
        if b2 >= 256 and b2-256 < len(ks): s += f'  Bk={ks[b2-256]!r}'
        if c >= 256 and c-256 < len(ks): s += f'  Ck={ks[c-256]!r}'
    return s

import sys
lo, hi = int(sys.argv[1]), int(sys.argv[2])
for i in range(lo, min(hi, sc)):
    print(f'[{i:3d}] {code[i]:08x} {ann(code[i])}')
