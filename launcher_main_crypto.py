# -*- coding: utf-8 -*-
# 主函数完整反汇编: 找 Crypto/decryptString/key 相关调用
import struct

buf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()
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

def rd_tstr(pos):
    if pos + 4 > len(buf): return None, pos
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0 or ln > 0x100000: return b'', pos + 4
    if pos + 4 + ln > len(buf): return None, pos
    return buf[pos+4:pos+4+ln-1], pos + 4 + ln

r = rd_tstr(12)
pos = r[1] + 12
sc = struct.unpack_from('<I', buf, pos)[0]
code = struct.unpack_from('<%dI' % sc, buf, pos + 4)
pos += 4 + sc * 4
sizek = struct.unpack_from('<I', buf, pos)[0]
pos += 4
ks = []
for i in range(sizek):
    t = buf[pos]; pos += 1
    if t == 0: ks.append(None)
    elif t == 1: ks.append(bool(buf[pos])); pos += 1
    elif t == 3: ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
    elif t == 4:
        rr = rd_tstr(pos); ks.append(rr[0]); pos = rr[1]

def show(i, ins):
    op = ins & 0x3F
    A = (ins >> 6) & 0xFF
    B = (ins >> 14) & 0x1FF
    C = (ins >> 23) & 0x1FF
    Bx = (ins >> 14) & 0x3FFFF
    nm = NAMES.get(op, 'OP%d' % op)
    extra = ''
    kk = None
    if nm in ('LOADK', 'GETGLOBAL') and Bx < len(ks) and ks[Bx]:
        kk = ks[Bx]
        extra = ' [%r]' % (kk,)
    return nm, A, B, C, Bx, extra, kk

# 全量反汇编到文件
out = []
for i, ins in enumerate(code):
    nm, A, B, C, Bx, extra, kk = show(i, ins)
    out.append('%5d %-10s A=%d B=%d C=%d Bx=%d%s' % (i, nm, A, B, C, Bx, extra))
open(r'C:\Users\20751\tomdump\launcher_main_disasm.txt', 'w', encoding='utf-8').write('\n'.join(out))

# 找关键常量 (Crypto/decrypt/encrypt/key/MD5/X1V5/16B)
keys = {}
for i, k in enumerate(ks):
    if isinstance(k, bytes):
        kl = k.lower()
        if any(x in kl for x in [b'crypt', b'decrypt', b'encrypt', b'md5', b'key', b'x1v5', b'secret']):
            keys[i] = k
            print('常量 k[%d] = %r' % (i, k))
print()
# 找引用这些常量的指令 + 上下文
for i, ins in enumerate(code):
    nm, A, B, C, Bx, extra, kk = show(i, ins)
    if kk is not None and any(idx == Bx for idx in keys):
        print('--- 指令 %d: %s %r ---' % (i, nm, kk))
        for j in range(max(0, i - 4), min(len(code), i + 10)):
            nm2, A2, B2, C2, Bx2, ex2, kk2 = show(j, code[j])
            print('    %5d %-10s A=%d B=%d C=%d Bx=%d%s' % (j, nm2, A2, B2, C2, Bx2, ex2))
        print()
