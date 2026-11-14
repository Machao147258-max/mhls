# -*- coding: utf-8 -*-
# 解码 launcher_raw.luac: 魔改 opcode 映射 + 反汇编加密子函数 (fn#2)
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()

def rd_tstr(pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

def walk(pos, depth, path):
    src, pos = rd_tstr(pos)
    pos += 12
    sc = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    code = struct.unpack_from('<%dI' % sc, buf, pos); pos += sc * 4
    sizek = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    ks = []
    for i in range(sizek):
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(bool(buf[pos])); pos += 1
        elif t == 3: ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            s, pos = rd_tstr(pos); ks.append(s)
        else:
            raise ValueError('const %d' % t)
    sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    protos = []
    for i in range(sizep):
        pr, pos = walk(pos, depth+1, path + '.' + str(i))
        protos.append(pr)
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    pos += n * 4
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos); pos += 8
    n = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for _ in range(n):
        _, pos = rd_tstr(pos)
    return {'src': src, 'code': code, 'k': ks, 'protos': protos, 'path': path}, pos

main, end = walk(12, 0, 'main')
print('解析完整 @', hex(end), '文件', len(buf))

# opcode 映射 (已知 + 推断)
# 标准 Lua 5.1 opcode 顺序: MOVE LOADK LOADBOOL LOADNIL GETUPVAL GETGLOBAL GETTABLE SETGLOBAL SETUPVAL SETTABLE NEWTABLE SELF ADD SUB MUL DIV MOD POW UNM NOT LEN CONCAT JMP EQ LT LE TEST TESTSET CALL TAILCALL RETURN FORLOOP FORPREP TFORLOOP SETLIST CLOSE CLOSURE VARARG
# 已知: LOADK=34, GETGLOBAL=20
# 从指令模式推断: 0x22(34)=LOADK, 0x4054(20)=GETGLOBAL
OPS = {}
OPS[34] = 'LOADK'
OPS[20] = 'GETGLOBAL'

def disasm(fn):
    print()
    print('==== %s  src=%s  code=%d k=%d ====' % (fn['path'], fn['src'], len(fn['code']), len(fn['k'])))
    for i, ins in enumerate(fn['code']):
        op = ins & 0x3F
        A = (ins >> 6) & 0xFF
        B = (ins >> 14) & 0x1FF
        C = (ins >> 23) & 0x1FF
        Bx = (ins >> 14) & 0x3FFFF
        nm = OPS.get(op, 'OP%d' % op)
        extra = ''
        if nm == 'LOADK' and Bx < len(fn['k']):
            extra = ' k[%d]=%r' % (Bx, fn['k'][Bx])
        if nm == 'GETGLOBAL' and Bx < len(fn['k']):
            extra = ' g[%d]=%r' % (Bx, fn['k'][Bx])
        print('  %5d %-10s A=%d B=%d C=%d Bx=%d%s' % (i, nm, A, B, C, Bx, extra))

# 找加密子函数 (含 Crypto/X1V5fzTo)
def find_crypto(fn, path=''):
    if any('Crypto' in str(x) or 'X1V5' in str(x) or 'encrypt' in str(x).lower() or 'FileMD5' == str(x) or b'FileMD5' == x for x in fn['k']):
        return fn
    for pr in fn['protos']:
        r = find_crypto(pr)
        if r: return r
    return None

c = find_crypto(main)
if c:
    disasm(c)
    # 也反汇编它的父函数 (调用者)
    def find_parent(fn, target, path=''):
        for pr in fn['protos']:
            if pr is target: return fn
            r = find_parent(pr, target)
            if r: return r
        return None
    p = find_parent(main, c)
    if p and p is not c:
        disasm(p)
else:
    print('未找到加密子函数')
