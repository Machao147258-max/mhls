# -*- coding: utf-8 -*-
# 反编译器 v2: 把 VM luac 还原为接近源码的结构化 Lua (识别 require/class/字段/表)
# 用法: python rev_decompiler.py <luac> [输出文件]
import struct, sys, os, re

def parse_proto(b, pos=12, depth=0):
    if pos + 4 > len(b): return None
    src_len = struct.unpack_from('<I', b, pos)[0]
    if src_len > 0x100000: return None
    pos += 4 + src_len
    pos += 12
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
                l2 = struct.unpack_from('<I', b, pos)[0]; pos += 4
                if l2 > 0x100000: return None
                pos += l2 + 8
        else:
            for _ in range(n):
                if pos + 4 > len(b): return None
                l2 = struct.unpack_from('<I', b, pos)[0]; pos += 4
                if l2 > 0x100000: return None
                pos += l2
    return pos, {'code': code, 'consts': consts, 'protos': protos}

def fmt_const(c):
    if c is None: return 'nil'
    if isinstance(c, bool): return 'true' if c else 'false'
    if isinstance(c, float):
        return repr(int(c)) if c == int(c) else repr(c)
    if isinstance(c, str):
        s = c.rstrip('\x00')
        return repr(s)
    return repr(c)

def kstr(consts, idx):
    if 0 <= idx < len(consts):
        return fmt_const(consts[idx])
    return f'K{idx}'

class Decompiler:
    def __init__(self, p):
        self.code = p['code']
        self.consts = p['consts']
        self.reg = {}      # reg -> 表达式
        self.regname = {}  # reg -> 变量名 (require 结果等)
        self.out = []
        self.used = 0

    def newvar(self, hint='v'):
        self.used += 1
        return f'{hint}_{self.used}'

    def rval(self, r):
        if r in self.regname:
            return self.regname[r]
        if r in self.reg:
            return self.reg[r]
        return f'<R{r}>'

    def run(self):
        i = 0
        n = len(self.code)
        while i < n:
            v = self.code[i]
            op = v & 0x3F
            a = (v >> 6) & 0xFF
            c = (v >> 23) & 0x1FF   # 高位 9 位 (本 VM: B/C 与标准相反!)
            b = (v >> 14) & 0x1FF   # 中位 9 位
            Bx = (v >> 14) & 0x3FFFF
            if op == 20:  # LOADK
                self.reg[a] = kstr(self.consts, Bx)
            elif op == 34:  # GETGLOBAL (Bx = 常量索引 = 全局名!)
                self.reg[a] = f'<GLOBAL {kstr(self.consts, Bx)}>'
            elif op == 4:  # CALL: 识别 require/class 模式
                args = [self.rval(r) for r in range(a + 1, a + b)]
                fn = self.rval(a)
                # 模式: <GLOBAL 'require'>(K) → 模块名
                m = re.match(r"<GLOBAL '(require|class)'>", fn)
                if m:
                    g = m.group(1)
                    mod = args[0].strip("'\"") if args else ''
                    if g == 'require' and args:
                        name = os.path.basename(mod).split('.')[0]
                        short = self.newvar(name)
                        self.out.append(f'local {short} = require({args[0]})')
                        self.regname[a] = short
                        self.reg[a] = short
                    elif g == 'class' and args:
                        short = self.newvar('Cls')
                        self.out.append(f'local {short} = class({args[0]})')
                        self.regname[a] = short
                        self.reg[a] = short
                    else:
                        self.out.append(f'{g}({", ".join(args)})')
                elif fn.startswith('<GLOBAL') and args:
                    g = fn.strip('<>').split(' ')[1]
                    self.out.append(f'{g}({", ".join(args)})')
                else:
                    self.out.append(f'{fn}({", ".join(args)})')
            elif op == 17:  # GETTABLE: R[a] = B表[C键] (B>=256 = K[B-256]!)
                if b >= 256:
                    tbl = kstr(self.consts, b - 256)
                else:
                    tbl = self.rval(b)
                if c >= 256:
                    key = kstr(self.consts, c - 256)
                else:
                    key = self.rval(c)
                self.reg[a] = f'{tbl}[{key}]'
            elif op == 36:  # op36: R[a][key(B)] = val(C)  (C>=256 = 常量索引 K[C-256]!)
                if b >= 256:
                    key = kstr(self.consts, b - 256)
                else:
                    key = kstr(self.consts, b)
                if c >= 256:
                    val = kstr(self.consts, c - 256)
                else:
                    val = self.rval(c)
                self.out.append(f'{self.rval(a)}[{key}] = {val}')
            elif op == 30:  # NEWTABLE
                var = self.newvar('t')
                self.reg[a] = var
                self.regname[a] = var
                self.out.append(f'local {var} = {{}}  -- NEWTABLE arr={c+1} hash={b+1}')
            elif op == 7:  # MOVE
                self.reg[a] = self.rval(b)
            elif op == 10:  # LOADIMM: R[A] = Bx 立即数
                self.reg[a] = str(Bx)
            elif op == 33:  # SELF: R[A] = R[B].K[C]
                if b >= 256:
                    t = self.rval(b)
                else:
                    t = self.rval(b)
                if c >= 256:
                    kk = self.rval(c)
                else:
                    kk = kstr(self.consts, c)
                self.reg[a] = f'{t}:{kk}'
            elif op == 18:  # CONCAT?
                B = (v >> 23) & 0xFF
                C = (v >> 14) & 0xFF
                parts = [self.rval(r) for r in range(B, C + 1)]
                self.reg[a] = ' .. '.join(parts)
            elif op == 5:  # RETURN
                pass
            else:
                self.reg[a] = f'<{op}:A{a} B{b} C{c}>'
            i += 1
        return '\n'.join(self.out)

def main(path):
    b = open(path, 'rb').read()
    r = parse_proto(b)
    if r is None:
        print('解析失败')
        return
    ep, p = r
    print(f'// 文件: {os.path.basename(path)}')
    print(f'// 顶层原型: code={len(p["code"])} consts={len(p["consts"])} protos={len(p["protos"])}')
    print()
    d = Decompiler(p)
    print(d.run())

if __name__ == '__main__':
    main(sys.argv[1])