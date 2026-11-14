# -*- coding: utf-8 -*-
# launcher 黄金验证反编译器 v2
# 已确认语义 (2026-08-11 实证):
#   C 中心: MOVE R[A]=R[C]; GETTABLE R[A]=R[C][B] (B=键 256+k 或寄存器)
#   LOADK/GETGLOBAL/SETGLOBAL: Bx 直接常量索引
#   CALL: fn=R[A], args=R[A+1..A+B+1] (nargs=B+1), 结果写 R[A], C=0 多返回
#   SELF: R[A]=R[C]:key, R[A+1]=R[C]
#   op16 CONCAT2: R[A]=R[C]..R[B]
#   op0 LT R[B]<R[C]; op22 EQ R[B]==R[C]; op14 TEST R[A] 真值
import struct, sys, re

import os
BUF_FILE = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\20751\tomdump\launcher_raw.luac'
OUT_DIR = sys.argv[2] if len(sys.argv) > 2 else None
buf = open(BUF_FILE, 'rb').read()

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
    if sc > 0x400000: raise ValueError('sc')
    code = list(struct.unpack_from('<%dI' % sc, buf, pos)); pos += sc*4
    sizek = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    if sizek > 0x100000: raise ValueError('sizek')
    ks = []
    for _ in range(sizek):
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(bool(buf[pos])); pos += 1
        elif t == 3: ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            s, pos = rd_tstr(pos); ks.append(s.decode('utf-8', 'replace'))
        else: raise ValueError('const')
    out.append((idx, src.decode('utf-8', 'replace'), sc, code, ks, depth))
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
except Exception:
    pass
print(f'解析出 {len(fns)} 个函数', flush=True)

def kstr(ks, i):
    if 0 <= i < len(ks):
        k = ks[i]
        if isinstance(k, str): return repr(k)
        return repr(k)
    return f'k[{i}]'

class Rev:
    def __init__(self, code, ks):
        self.code = code
        self.ks = ks
        self.r = {}       # reg -> 表达式
        self.var = {}     # reg -> 变量名
        self.selfof = {}  # reg -> table 表达式 (SELF 产生的方法寄存器)
        self.out = []
        self.used = 0
        self.labels = {}
        self.jumps = {}   # i -> 目标标签
    def nv(self, hint='v'):
        self.used += 1
        return f'{hint}{self.used}'
    def defined(self, i):
        return i in self.r or i in self.var
    def rval(self, i):
        if i in self.var: return self.var[i]
        if i in self.r: return self.r[i]
        return f'R{i}'
    def set(self, i, expr, hint='v'):
        if i in self.var:
            self.out.append(f'{self.var[i]} = {expr}')
            self.r[i] = expr
        elif i in self.r and self.r[i] == expr:
            pass
        else:
            v = self.nv(hint)
            self.var[i] = v
            self.r[i] = expr
            self.out.append(f'local {v} = {expr}')
    def run(self):
        code = self.code
        n = len(code)
        for i, v in enumerate(code):
            op = v & 0x3F
            if op == 21:
                sbx = ((v >> 14) & 0x3FFFF) - 131071
                t = i + 1 + sbx
                self.labels.setdefault(t, len(self.labels))
                self.jumps[i] = t
        i = 0
        while i < n:
            v = code[i]
            op = v & 0x3F
            a = (v >> 6) & 0xFF
            b = (v >> 14) & 0x1FF
            c = (v >> 23) & 0x1FF
            bx = (v >> 14) & 0x3FFFF
            sbx = bx - 131071
            if i in self.labels:
                self.out.append(f'-- L{self.labels[i]}:')
            if op == 7:  # MOVE R[A]=R[C]
                self.set(a, self.rval(c), 'v')
            elif op == 20:  # LOADK R[A]=k[Bx] (直接索引)
                self.set(a, kstr(self.ks, bx), 'c')
            elif op == 34:  # GETGLOBAL
                self.set(a, f'<G {kstr(self.ks, bx)}>', 'g')
            elif op == 12:  # SETGLOBAL global[k[Bx]]=R[A]
                self.out.append(f'<G {kstr(self.ks, bx)}> = {self.rval(a)}')
            elif op == 17:  # GETTABLE R[A]=R[C][B]
                key = kstr(self.ks, b-256) if b >= 256 else self.rval(b)
                self.set(a, f'{self.rval(c)}[{key}]', 't')
            elif op == 33:  # SELF R[A]=R[C]:key, R[A+1]=R[C]
                key = kstr(self.ks, b-256) if b >= 256 else self.rval(b)
                tbl = self.rval(c)
                self.set(a, f'{tbl}:{key}', 'm')
                self.selfof[a] = tbl
                self.set(a+1, tbl, 's')
            elif op == 4:  # CALL fn=R[A] args=R[A+1..A+B+1]
                fn = self.rval(a)
                args = []
                for j in range(a+1, a + b + 2):
                    if j >= n: break
                    if not self.defined(j): break  # 尾部未定义 → 裁剪
                    args.append(self.rval(j))
                # SELF 冒号语法: 第一个参数 == self 表
                if a in self.selfof and args and args[0] == self.selfof[a]:
                    args = args[1:]
                    expr = f'{self.selfof[a]}:{fn.split(":", 1)[1]}({", ".join(args)})' if ':' in fn else f'{fn}({", ".join(args)})'
                else:
                    expr = f'{fn}({", ".join(args)})'
                self.set(a, expr, 'r')
            elif op == 36:  # SETTABLEK R[A][k] = v
                key = kstr(self.ks, c-256) if c >= 256 else self.rval(c)
                val = kstr(self.ks, b-256) if b >= 256 else self.rval(b)
                self.out.append(f'{self.rval(a)}[{key}] = {val}')
            elif op == 30:  # NEWTABLE
                self.set(a, '{}', 't')
            elif op in (28, 31):  # LOADNIL/LOADNIL2
                self.set(a, 'nil', 'n')
            elif op == 10:  # LOADIMM (语义未定)
                self.set(a, f'<imm{bx}>', 'i')
            elif op == 16:  # CONCAT2 R[A]=R[C]..R[B]
                self.set(a, f'{self.rval(c)} .. {self.rval(b)}', 's')
            elif op == 18:  # CONCAT (范围, 简化为二元)
                self.set(a, f'{self.rval(c)} .. {self.rval(b)}', 's')
            elif op == 22:  # EQ R[B] cmp R[C], A=1 → 不等跳
                lb = kstr(self.ks, b-256) if b >= 256 else self.rval(b)
                lc = kstr(self.ks, c-256) if c >= 256 else self.rval(c)
                tgt = self.jumps.get(i+1)
                tgt2 = self.jumps.get(i)
                if tgt is not None:
                    self.out.append(f'-- if {lb} {"~=" if a else "=="} {lc} goto L{tgt}')
                elif tgt2 is not None:
                    self.out.append(f'-- if {lb} {"==" if a else "~="} {lc} goto L{tgt2}')
                else:
                    self.out.append(f'-- EQ {lb} {"!=" if a else "=="} {lc}')
            elif op == 0:  # LT R[B]<R[C], A=0 → 真跳
                lb = kstr(self.ks, b-256) if b >= 256 else self.rval(b)
                lc = kstr(self.ks, c-256) if c >= 256 else self.rval(c)
                tgt = self.jumps.get(i+1) or self.jumps.get(i)
                self.out.append(f'-- if {lb} < {lc} {"goto L%d" % tgt if tgt is not None else ""}')
            elif op == 1:  # LE
                lb = kstr(self.ks, b-256) if b >= 256 else self.rval(b)
                lc = kstr(self.ks, c-256) if c >= 256 else self.rval(c)
                tgt = self.jumps.get(i+1) or self.jumps.get(i)
                self.out.append(f'-- if {lb} <= {lc} {"goto L%d" % tgt if tgt is not None else ""}')
            elif op == 14:  # TEST R[A]
                tgt = self.jumps.get(i+1)
                self.out.append(f'-- if not {self.rval(a)} {"goto L%d" % tgt if tgt is not None else ""}')
            elif op == 2:  # TESTSET
                self.set(a, self.rval(b), 'v')
            elif op == 21:  # JMP
                self.out.append(f'-- goto L{self.labels.get(i+1+sbx, "?")}')
            elif op == 5:  # RETURN
                self.out.append(f'return {self.rval(a)}')
            elif op == 9:  # CALLSETUP
                pass
            elif op == 3:  # LOADBOOL
                self.set(a, 'true' if b else 'false', 'b')
            else:
                self.out.append(f'-- op{op} A={a} B={b} C={c}')
            i += 1

parts = []
for idx, src, sc, code, ks, depth in fns:
    parts.append(f'\n===== fn#{idx} {src!r} ({sc} instr, depth {depth}) =====')
    r = Rev(code, ks)
    r.run()
    parts.append('\n'.join(r.out))
txt = '\n'.join(parts)
if OUT_DIR:
    os.makedirs(OUT_DIR, exist_ok=True)
    base = os.path.basename(BUF_FILE).replace('.luac', '')
    out_path = os.path.join(OUT_DIR, base + '.rev.lua')
    open(out_path, 'w', encoding='utf-8').write(txt)
    print(f'OK {out_path} ({len(txt)}B, {len(fns)} fns)', flush=True)
else:
    print(txt, flush=True)
