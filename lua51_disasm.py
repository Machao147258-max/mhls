# -*- coding: utf-8 -*-
# 迷你 Lua 5.1 反汇编: 验证 chunk 指令是否标准 + 结构一致性
# 用法: python lua51_disasm.py <chunk.luac> [max_instr]
import sys, struct

OPS = ['MOVE','LOADK','LOADBOOL','LOADNIL','GETUPVAL','GETGLOBAL','GETTABLE','SETGLOBAL',
       'SETUPVAL','SETTABLE','NEWTABLE','SELF','ADD','SUB','MUL','DIV','MOD','POW','UNM',
       'NOT','LEN','CONCAT','JMP','EQ','LT','LE','TEST','TESTSET','CALL','TAILCALL','RETURN',
       'FORLOOP','FORPREP','TFORLOOP','SETLIST','CLOSE','CLOSURE','VARARG']

def u32(b, o): return struct.unpack_from('<I', b, o)[0]

def parse(b, p, dump):
    """5.1 解析;dump=True 时打印顶层代码"""
    def rs():
        nonlocal p
        l = u32(b, p); p += 4
        s = b[p:p + max(l - 1, 0)].decode('latin-1', 'replace') if 0 < l < 4096 else ''
        p += l
        return s
    src = rs()
    p += 4 + 4 + 4
    ncode = u32(b, p); p += 4
    code = [u32(b, p + i * 4) for i in range(ncode)]
    p += ncode * 4
    nk = u32(b, p); p += 4
    k = []
    for _ in range(nk):
        t = b[p]; p += 1
        if t == 0: k.append('nil')
        elif t == 1: k.append(str(b[p])); p += 1
        elif t == 3: k.append(struct.unpack_from('<d', b, p)[0]); p += 8
        elif t == 4: k.append(rs())
    if dump:
        print(f';; {src}  ncode={ncode} nk={nk} nk展示={k[:20]}')
        for i, ins in enumerate(code):
            op = ins & 0x3F; A = (ins >> 6) & 0xFF
            B = (ins >> 14) & 0x1FF; C = (ins >> 23) & 0x1FF
            Bx = (ins >> 14) & 0x3FFFF; sBx = Bx - 131071
            nm = OPS[op] if op < len(OPS) else f'OP{op}'
            extra = ''
            if op in (1, 5, 7, 12, 13, 14, 15, 16, 17, 24, 25, 26, 37):
                extra = f' k[{Bx}]={k[Bx] if Bx < len(k) else "?"}' if op in (1, 5, 7) else ''
            print(f'  {i:5d} {nm:<10} A={A:<4} B={B:<5} C={C:<5} Bx={Bx}{extra}')
    # 常量已读;跳 debug
    n = u32(b, p); p += 4 + n
    n = u32(b, p); p += 4
    for _ in range(n):
        rs(); p += 8
    n = u32(b, p); p += 4
    for _ in range(n):
        rs()
    n = u32(b, p); p += 4
    for _ in range(n):
        p = parse(b, p, False)
    return p

if __name__ == '__main__':
    fn = sys.argv[1]
    mx = int(sys.argv[2]) if len(sys.argv) > 2 else 80
    b = open(fn, 'rb').read()
    hdr_ok = b[:12] == b'\x1bLua\x51\x00\x01\x04\x04\x04\x08\x00'
    print('header:', '标准Lua5.1(dbl)' if hdr_ok else '异常! ' + b[:12].hex())
    end = parse(b, 12, True)
    print('解析结束偏移:', end, '/ 文件大小:', len(b), '→', '完整' if end == len(b) else '不完整(差 %d)' % (len(b) - end))