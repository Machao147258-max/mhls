# -*- coding: utf-8 -*-
# 用 launcher 常量表(全局名字表)反编译 common_utils — 验证全局槽号方案
import struct, sys, os
sys.path.insert(0, r'C:\Users\20751\Desktop\猫和老鼠')
import launcher_rev as L

# 加载 launcher 的常量表作为名字表
lbuf = open(r'C:\Users\20751\tomdump\launcher_raw.luac', 'rb').read()
# 从 launcher 提取主函数 ks
def extract_ks(buf):
    p = 12
    ln = struct.unpack_from('<I', buf, p)[0]; p += 4 + ln
    p += 12
    sc = struct.unpack_from('<I', buf, p)[0]; p += 4 + sc * 4
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
    return ks

names = extract_ks(lbuf)
print(f'名字表 {len(names)} 项', flush=True)
print('前 20:', names[:20], flush=True)

# 反编译 common_utils, 用名字表替代空 ks
buf = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac', 'rb').read()

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
print(f'解析 {len(fns)} 函数', flush=True)

# 修补: 空 ks 的函数用名字表
for idx, src, sc, code, ks, depth in fns:
    if len(ks) < 5:
        ks[:] = names[:]
    r = L.Rev(code, ks)
    r.run()
    print(f'\n===== fn#{idx} {src!r} ({sc} instr) =====', flush=True)
    print('\n'.join(r.out), flush=True)
