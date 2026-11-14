# -*- coding: utf-8 -*-
# 扫描指定 luac 中未知 op 的上下文 (实证语义)
import struct, sys

sys.path.insert(0, r'C:\Users\20751\Desktop\猫和老鼠')
SO = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so','rb').read()
FMT = SO[0xcd3820:0xcd3820+42]
NAMES = {0:'LT',1:'LE',2:'TESTSET',3:'LOADBOOL',4:'CALL',5:'RETURN',6:'FORLOOP',7:'MOVE',8:'FORPREP',9:'CALLSETUP',10:'LOADIMM',11:'GETUPVAL',12:'SETGLOBAL',13:'CLOSE',14:'TEST',15:'TAILCALL',16:'LEN',17:'GETTABLE',18:'CONCAT',19:'ADD',20:'LOADK',21:'JMP',22:'EQ',23:'FORCOND',24:'SUB',25:'GETTABLE2',26:'SETUPVAL',27:'MUL',28:'LOADNIL',29:'NOT',30:'NEWTABLE',31:'LOADNIL2',32:'DIV',33:'SELF',34:'GETGLOBAL',35:'ARITH',36:'SETTABLEK',37:'VARARG'}

def analyze(fn, targets):
    buf = open(fn, 'rb').read()
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
        if sc > 0x200000: raise ValueError('sc')
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
        out.append((idx, src, sc, code, ks))
        sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
        for i in range(sizep):
            try:
                pos = walk(pos, depth+1, i, out)
            except Exception:
                return pos
        return pos
    fns = []
    try:
        walk(12, 0, 0, fns)
    except Exception as e:
        pass
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
        if b2 >= 256 and b2-256 < len(ks): ann += f' B=k{kk(ks,b2-256)}'
        if c >= 256 and c-256 < len(ks): ann += f' C=k{kk(ks,c-256)}'
        if op in (20, 34):
            ki = bx - 256 if op == 20 else bx
            if 0 <= ki < len(ks): ann += f' Bx=k{kk(ks,ki)}'
        if mode == 1: return f'{name:9s} A={a:3d} Bx={bx:5d}{ann}'
        if mode == 2: return f'{name:9s} A={a:3d} sBx={bx-131071:6d}{ann}'
        return f'{name:9s} A={a:3d} B={b2:3d} C={c:3d}{ann}'
    print(f'===== {fn} ({len(fns)} fns) =====')
    found = {}
    for idx, src, sc, code, ks in fns:
        for i, v in enumerate(code):
            op = v & 0x3F
            if op not in targets: continue
            if found.get(op, 0) >= 1: continue
            found[op] = 1
            lo, hi = max(0, i-3), min(sc, i+4)
            print(f'--- fn#{idx} [{i}] ---')
            for j in range(lo, hi):
                mark = '>>' if j == i else '  '
                print(f'{mark}[{j:3d}] {fmt_ins(code[j], ks)}')
    missing = [op for op in targets if op not in found]
    print('未见:', missing)
    return missing

if __name__ == '__main__':
    import glob, os
    t = {1, 3, 11, 13, 15, 19, 24, 26, 27, 29, 32, 37}
    for f in sys.argv[1:] or [r'C:\Users\20751\tomdump\mega_luac\src_catchGame_systems_GmSystem.lua.luac',
                              r'C:\Users\20751\tomdump\mega_luac\src_catchGame_data_role.lua.luac',
                              r'C:\Users\20751\tomdump\mega_luac\src_catchGame_systems_SquareSystem.lua.luac',
                              r'C:\Users\20751\tomdump\mega_luac\src_catchGame_box2d_RubeSceneReader.lua.luac',
                              r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac']:
        try:
            analyze(f, t)
        except Exception as e:
            print(f'ERR {f}: {e}')
