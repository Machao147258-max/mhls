# -*- coding: utf-8 -*-
# 解析 x11_luac (common/utils.lua 完整明文) 全部函数, 找 Crypto/decrypt/key
import struct, sys, os

sys.path.insert(0, r'C:\Users\20751\Desktop\猫和老鼠')
buf = open(r'C:\Users\20751\tomdump\live_segs\x11_luac.bin', 'rb').read()
# 找到 luac 头
i = buf.find(b'\x1bLuaQ')
print(f'luac @ {hex(i)}, 总 {len(buf)}B')

def rd_tstr(pos):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln == 0: return b'', pos + 4
    s = buf[pos+4:pos+4+ln]
    return s[:-1], pos + 4 + ln

out = []
def walk(pos, depth, idx):
    ln = struct.unpack_from('<I', buf, pos)[0]
    if ln > 0x100000: raise ValueError('src')
    src, pos = rd_tstr(pos)
    pos += 12
    sc = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    if sc > 0x400000: raise ValueError('sc')
    code = list(struct.unpack_from('<%dI' % sc, buf, pos)); pos += sc*4
    sizek = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    ks = []
    for _ in range(sizek):
        t = buf[pos]; pos += 1
        if t == 0: ks.append(None)
        elif t == 1: ks.append(bool(buf[pos])); pos += 1
        elif t == 3: ks.append(struct.unpack_from('<d', buf, pos)[0]); pos += 8
        elif t == 4:
            s, pos = rd_tstr(pos); ks.append(s.decode('utf-8', 'replace'))
        else: raise ValueError('const')
    out.append((idx, src, sc, code, ks, depth, pos))
    sizep = struct.unpack_from('<I', buf, pos)[0]; pos += 4
    for k in range(sizep):
        try:
            pos = walk(pos, depth+1, k)
        except Exception:
            return pos
    return pos

try:
    walk(i + 12, 0, 0)
except Exception as e:
    print('walk err', e)
print(f'解析 {len(out)} 函数')
# 找含关键词的函数
KW = [b'Crypto', b'decrypt', b'encrypt', b'X1V5fzTo', b'xxtea', b'XXTEA', b'key', b'Key', b'getStringFromFile']
for idx, src, sc, code, ks, depth, pos in out:
    hits = [kk for kk in ks if isinstance(kk, str) and any(w.decode('utf-8','replace').lower() in kk.lower() for w in [b'crypto', b'decrypt', b'encrypt', b'x1v5', b'xxtea'])]
    if hits:
        print(f'\n=== fn#{idx} src={src!r} {sc} instr {len(ks)} consts (depth {depth}) ===')
        print(f'  关键词常量: {hits}')
        # 打印全部字符串常量
        strs = [k for k in ks if isinstance(k, str) and len(k) >= 4]
        print(f'  全部字符串常量 ({len(strs)}):')
        for s in strs[:60]:
            print(f'    {s!r}')
