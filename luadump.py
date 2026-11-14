# -*- coding: utf-8 -*-
"""Dump Lua 5.1 chunk: proto tree, constants (name-ordered), and disassembly."""
import io, os, sys, struct, tarfile

OPNAMES = ['MOVE','LOADK','LOADBOOL','LOADNIL','GETUPVAL','GETGLOBAL','GETTABLE','SETGLOBAL',
'SETUPVAL','SETTABLE','NEWTABLE','SELF','ADD','SUB','MUL','DIV','MOD','POW','UNM','NOT','LEN',
'CONCAT','JMP','EQ','LT','LE','TEST','TESTSET','CALL','TAILCALL','RETURN','FORLOOP','FORPREP',
'TFORLOOP','SETLIST','CLOSE','CLOSURE','VARARG']

class RD:
    def __init__(s, f): s.f = f
    def u8(s):
        d = s.f.read(1)
        if not d: raise EOFError
        return d[0]
    def i32(s):
        d = s.f.read(4)
        if len(d) < 4: raise EOFError
        return struct.unpack('<i', d)[0]
    def u32(s):
        d = s.f.read(4)
        if len(d) < 4: raise EOFError
        return struct.unpack('<I', d)[0]
    def dbl(s):
        d = s.f.read(8)
        if len(d) < 8: raise EOFError
        return struct.unpack('<d', d)[0]
    def str(s):
        n = s.i32()
        if n == 0: return ''
        d = s.f.read(n)
        return d[:-1].decode('utf-8', 'replace')

def read_func(r, out, depth=0):
    src = r.str()
    linedef = r.i32(); lastline = r.i32()
    nups = r.u8(); numparams = r.u8(); isvarg = r.u8(); maxstack = r.u8()
    node = {'src': src, 'line': linedef, 'lastline': lastline, 'nups': nups,
            'nparams': numparams, 'maxstack': maxstack, 'k': [], 'insn': [], 'kids': [],
            'upnames': []}
    n = r.i32()
    for _ in range(n):
        node['insn'].append(r.u32())
    nk = r.i32()
    for _ in range(nk):
        t = r.u8()
        if t == 0: node['k'].append(('nil', None))
        elif t == 1: node['k'].append(('bool', r.u8()))
        elif t == 3: node['k'].append(('num', r.dbl()))
        elif t == 4: node['k'].append(('str', r.str()))
        else: raise ValueError('const %d' % t)
    np = r.i32()
    for _ in range(np):
        node['kids'].append(read_func(r, out, depth + 1))
    n = r.i32(); r.f.read(n * 4)          # lineinfo
    n = r.i32()
    for _ in range(n):
        r.str(); r.i32(); r.i32()          # locvars
    n = r.i32()
    for _ in range(n):
        node['upnames'].append(r.str())
    return node

def disasm(node, out, idx):
    out.append('===== proto#%d  src=%s  lines=%d-%d  nparams=%d nups=%d maxstack=%d =====' %
               (idx[0], node['src'].lstrip('@'), node['line'], node['lastline'],
                node['nparams'], node['nups'], node['maxstack']))
    out.append('  upvalues: %s' % (node['upnames'],))
    out.append('  constants: %s' % ([(t, v) for t, v in node['k']],))
    for pc, w in enumerate(node['insn']):
        op = w & 0x3F
        a = (w >> 6) & 0xFF
        c = (w >> 14) & 0x1FF
        b = (w >> 23) & 0x1FF
        bx = (w >> 14) & 0x3FFFF
        sbx = bx - 131071
        nm = OPNAMES[op] if op < len(OPNAMES) else 'OP%d' % op
        extra = ''
        if nm in ('LOADK', 'GETGLOBAL', 'SETGLOBAL'):
            extra = ' K%d=%s' % (bx, node['k'][bx] if bx < len(node['k']) else '?')
        elif nm in ('GETTABLE', 'SETTABLE', 'SELF'):
            extra = ' K%dc=%s' % (c, node['k'][c] if c < len(node['k']) else '?')
        out.append('   %4d  %-14s A=%-3d B=%-4d C=%-4d Bx=%-6d sBx=%-6d%s' % (pc, nm, a, b, c, bx, sbx, extra))
    for j, kid in enumerate(node['kids']):
        out.append('')
        out.append('  --- child of proto#%d : kid#%d ---' % (idx[0], j))
        disasm(kid, out, idx)
    idx[0] += 1

def main():
    tar, member, dst = sys.argv[1], sys.argv[2], sys.argv[3]
    with tarfile.open(tar) as t:
        data = t.extractfile(t.getmember(member)).read()
    r = RD(io.BytesIO(data))
    r.f.read(12)
    out = ['chunk=%s  size=%d' % (member, len(data))]
    root = read_func(r, out)
    disasm(root, out, [0])
    io.open(dst, 'w', encoding='utf-8').write('\n'.join(out))
    print('wrote %s (%d lines)' % (dst, len(out)))

main()
