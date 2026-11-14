# -*- coding: utf-8 -*-
# 用验证过的 walker 定位 fn#2 并解码指令(带常量解析)
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()
SO = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so','rb').read()
FMT = SO[0xcd3820:0xcd3820+42]
NAMES = {0:'LT?',1:'LE?',2:'TESTSET',3:'LOADBOOL',4:'CALL',5:'RETURN',6:'FORLOOP?',7:'MOVE',8:'FORPREP?',9:'CALLSETUP',10:'LOADIMM',11:'GETUPVAL?',12:'SETGLOBAL?',13:'CLOSE?',14:'TEST',15:'TAILCALL?',16:'LEN?',17:'GETTABLE',18:'CONCAT?',19:'ADD?',20:'LOADK',21:'JMP',22:'EQ',23:'FORCOND?',24:'SUB?',25:'GETTABLE2',26:'SETUPVAL?',27:'MUL?',28:'LOADNIL?',29:'NOT?',30:'NEWTABLE',31:'LOADNIL2?',32:'DIV?',33:'SELF',34:'GETGLOBAL',35:'ARITH',36:'SETTABLEK',37:'VARARG?'}

def rd_tstr(pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

def dump_code(code, ks):
    for j, v in enumerate(code):
        op = v & 0x3F; a = (v >> 6) & 0xFF
        b2 = (v >> 14) & 0x1FF; c = (v >> 23) & 0x1FF
        bx = (v >> 14) & 0x3FFFF; sbx = bx - 131071
        mode = FMT[op] & 3 if op < 42 else 0
        name = NAMES.get(op, f'op{op}')
        ann = ''
        if op in (17, 25, 33, 36):
            if b2 >= 256 and b2 - 256 < len(ks): ann += f' B=k[{b2-256}]={ks[b2-256]!r}'
            if c >= 256 and c - 256 < len(ks): ann += f' C=k[{c-256}]={ks[c-256]!r}'
        if op in (20, 34):
            ki = bx - 256 if op == 20 else bx
            if 0 <= ki < len(ks): ann += f' Bx=k[{ki}]={ks[ki]!r}'
        if mode == 2:
            print(f'[{j:3d}] {v:08x} {name:9s} A={a:3d} sBx={sbx:6d}{ann}')
        elif mode == 1:
            print(f'[{j:3d}] {v:08x} {name:9s} A={a:3d} Bx={bx:5d}{ann}')
        else:
            print(f'[{j:3d}] {v:08x} {name:9s} A={a:3d} B={b2:3d} C={c:3d}{ann}')

def walk(pos, depth, idx):
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
        else: raise ValueError(f'const {t}')
    if idx == 2:
        print(f'=== fn#{idx} src={src!r} sc={sc} k={sizek} ===')
        for i, kk in enumerate(ks): print(f'  k[{i}] = {kk!r}')
        dump_code(code, ks)
        raise SystemExit
    sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for i in range(sizep):
        pos = walk(pos, depth+1, i)
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    pos += n*4
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos); pos += 8
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos)
    return pos

walk(12, 0, 0)
