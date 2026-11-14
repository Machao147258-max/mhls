# -*- coding: utf-8 -*-
"""libepay-crypto.so: 全量节表 + 定位 0xd10f0/0xd110a/0xd1138 的节归属与初始值"""
import struct
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()
N = len(d)
print("file size = %#x" % N)

e_shoff = struct.unpack_from('<Q', d, 40)[0]
e_shentsize, e_shnum, e_shstrndx = struct.unpack_from('<HHH', d, 58)
secs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack_from('<IIQQQQ', d, off)
    secs.append((sh_name, sh_type, sh_addr, sh_offset, sh_size))
shstr_off = secs[e_shstrndx][3]
def shname(no):
    e = shstr_off + no; z = d.index(b'\x00', e); return d[e:z].decode('latin1')

print("\n== 节表 (name addr off size) ==")
for s in secs:
    print("  %-18s addr=%#-9x off=%#-9x size=%#x" % (shname(s[0]), s[2], s[3], s[4]))

def va_of(va):
    for _, _, a, o, sz in secs:
        if a <= va < a + sz and sz > 0:
            return o + (va - a), shname([x[0] for x in secs].index(*[s0 for s0 in secs if s0[2]==a][0][0])) if False else None
    return None, None

print("\n== 关键 VA 定位 ==")
for va in (0xd10d0, 0xd10f0, 0xd110a, 0xd1138, 0xd1148, 0xd1110):
    hit = None; nm = None
    for (sn, st, a, o, sz) in secs:
        if sz and a <= va < a + sz:
            hit = (o + (va - a)); nm = shname(sn); break
    if hit is not None:
        val = d[hit:hit+16]
        print("  VA %#x -> 节 %-12s off=%#x 16B预览: %s" % (va, nm, hit, val.hex()))
    else:
        print("  VA %#x -> 不在任何节 (bss?)" % va)