# -*- coding: utf-8 -*-
"""parse_elf_sym.py — 解析 ELF 动态符号表(绕过混淆的 section header, 用 PT_DYNAMIC)"""
import struct

SO = r'C:\Users\20751\tomdump\device_libs\libcocos2dlua.so'
d = open(SO, 'rb').read()
e_phoff = struct.unpack_from('<Q', d, 0x20)[0]
e_phentsize = struct.unpack_from('<H', d, 0x36)[0]
e_phnum = struct.unpack_from('<H', d, 0x38)[0]

phdrs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    t = struct.unpack_from('<I', d, o)[0]
    off = struct.unpack_from('<Q', d, o + 8)[0]
    va = struct.unpack_from('<Q', d, o + 0x10)[0]
    sz = struct.unpack_from('<Q', d, o + 0x20)[0]
    phdrs.append((t, off, va, sz))

# PT_DYNAMIC = 2
dyn = [p for p in phdrs if p[0] == 2][0]
dyn_off, dyn_va = dyn[1], dyn[2]

dyns = {}
for i in range(0, dyn[3], 16):
    tag = struct.unpack_from('<q', d, dyn_off + i)[0]
    val = struct.unpack_from('<Q', d, dyn_off + i + 8)[0]
    dyns[tag] = val

# DT_STRTAB=5, DT_SYMTAB=6, DT_STRSZ=10, DT_SYMENT=11, DT_GNU_HASH=0x6ffffef5, DT_HASH=4
strtab = dyns.get(5)
symtab = dyns.get(6)
strsz = dyns.get(10)
syment = dyns.get(11) or 24
print(f'dynsym @ {symtab:#x}, strtab @ {strtab:#x}')

def va2off(va):
    for t, o, v, s in phdrs:
        if t == 1 and v <= va < v + s:
            return o + (va - v)
    return None

n = 0
i = 0
syms = []
while True:
    off = va2off(symtab + i * syment)
    if off is None:
        break
    st_name = struct.unpack_from('<I', d, off)[0]
    st_info = d[off + 4]
    st_value = struct.unpack_from('<Q', d, off + 8)[0]
    st_size = struct.unpack_from('<Q', d, off + 16)[0]
    if st_name:
        s_off = va2off(strtab + st_name)
        name = None
        if s_off is not None:
            end = d.find(b'\x00', s_off)
            name = d[s_off:end].decode('latin-1', 'replace')
        if name and (st_value or st_size):
            syms.append((name, st_value, st_size, st_info))
            n += 1
    i += 1
    if i > 200000:
        break
print('符号总数:', n)
# 找有趣的
import re
crypto = [s for s in syms if re.search(r'crypt|aes|rsa|undump|loadbuffer|luaU|decrypt|encrypt|dun|sec', s[0], re.I)]
print('crypto 相关:', len(crypto))
for name, va, sz, info in crypto[:40]:
    print(f'  {name[:90]:<92} va={va:#x} size={sz:#x}')