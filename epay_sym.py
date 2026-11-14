# -*- coding: utf-8 -*-
"""libepay-crypto.so: .dynsym 全符号检索 + 目标函数名定位"""
import struct
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()

e_shoff = struct.unpack_from('<Q', d, 40)[0]
e_shentsize, e_shnum, e_shstrndx = struct.unpack_from('<HHH', d, 58)
secs = {}
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack_from('<IIQQQQ', d, off)
    secs[i] = dict(name_off=sh_name, addr=sh_addr, off=sh_offset, size=sh_size, entsz=struct.unpack_from('<Q', d, off+56)[0])
shstr_off = secs[e_shstrndx]['off']
def shname(no):
    e = shstr_off + no; z = d.index(b'\x00', e); return d[e:z].decode('latin1')
names = [shname(s['name_off']) for s in secs.values()]
dynsym = secs[names.index('.dynsym')]; dynstr = secs[names.index('.dynstr')]
doff = dynstr['off']

print("== dynsym 中含 Aes/Secret/Cipher/key/epay/base64 的符号 ==")
ENT = dynsym['entsz'] or 24
for e in range(dynsym['size'] // ENT):
    st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from('<IBBHQQ', d, dynsym['off'] + e * ENT)
    if st_name == 0: continue
    nm = d[doff + st_name:].split(b'\x00')[0].decode('latin1', 'replace')
    low = nm.lower()
    if any(k in low for k in ('aes', 'secret', 'cipher', 'key', 'epay', 'crypto', 'base64', 'decode', 'encode')):
        print("  %#x  %s" % (st_value, nm))

print("\n== .dynstr 中 getAesKey / getFlexibleSecret / 方法名 ==")
for pat in (b'getAesKey', b'getFlexibleSecret', b'base64Encode', b'base64Decode', b'getSecret', b'decrypt', b'encrypt'):
    pos = 0
    while True:
        i = d.find(pat, pos)
        if i < 0: break
        print("  %#x : %s" % (i, d[i:i+64].split(b'\x00')[0].decode('latin1', 'replace')))
        pos = i + 1