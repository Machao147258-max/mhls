# -*- coding: utf-8 -*-
"""全文件搜索 SSL version 小整数 (0x300/0x301/0x302/0x303), 检查周围布局与所在段"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def off2v(o):
    if 0 <= o < 0x10022b8: return o
    if 0x1002e08 <= o < 0x1580540: return o + 0x10000
    if 0x1574000 <= o < 0x1906000: return o + 0x3d000
    return None

VERSIONS = {0x300: 'SSLv3', 0x301: 'TLSv1', 0x302: 'TLSv1.1', 0x303: 'TLSv1.2'}
hits = {v: 0 for v in VERSIONS}

# 全文件 8 字节步进扫描 version (低4字节匹配)
for o in range(0, len(d) - 32, 8):
    q = struct.unpack_from('<Q', d, o)[0]
    v = q & 0xFFFFFFFF
    if v in VERSIONS:
        hits[v] += 1
        if hits[v] <= 3:
            va = off2v(o)
            if o + 72 > len(d):
                continue
            nxt = struct.unpack_from('<9Q', d, o)
            print(f"--- version={VERSIONS[v]} ({v:#06x}) @ fileoff {o:#x} vaddr {va if va else '??'} ---")
            print(f"    q1(new)={nxt[1]:#x} q2(clear)={nxt[2]:#x} q3(free)={nxt[3]:#x}")
            print(f"    q4(acc)={nxt[4]:#x} q5(con)={nxt[5]:#x} q6(read)={nxt[6]:#x} q7(peek)={nxt[7]:#x} q8(wr)={nxt[8]:#x}")

print(f"\n命中统计: { {VERSIONS[k]: v for k, v in hits.items()} }")