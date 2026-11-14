# -*- coding: utf-8 -*-
"""libepay-crypto.so: ELF 节表解析 + JNI 导出函数地址 + getAesKey/getFlexibleSecret 反汇编"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()

# ELF64 header
magic, e_class, e_data, e_ver, osabi = d[0:4], d[4], d[5], d[6], d[7]
e_type, e_machine, e_version = struct.unpack_from('<HHI', d, 16)
e_entry, e_phoff, e_shoff = struct.unpack_from('<QQQ', d, 24)
e_flags, e_ehsize = struct.unpack_from('<IH', d, 48)
e_phentsize, e_phnum, e_shentsize, e_shnum, e_shstrndx = struct.unpack_from('<HHHHH', d, 54)
print("machine=0x%x (%s) type=0x%x shnum=%d" % (e_machine, {0xb7:'AArch64',0x3e:'x86_64',0x28:'ARM',0x3:'x86'}.get(e_machine,'?'), e_type, e_shnum))

# 节表
secs = {}
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack_from('<IIQQQQ', d, off)
    secs[i] = dict(name_off=sh_name, type=sh_type, addr=sh_addr, off=sh_offset, size=sh_size, entsz=struct.unpack_from('<Q', d, off+56)[0])

shstr_off = secs[e_shstrndx]['off']
def shname(no):
    e = shstr_off + no
    z = d.index(b'\x00', e)
    return d[e:z].decode('latin1')

for i, s in secs.items():
    n = shname(s['name_off'])
    if n in ('.dynsym', '.dynstr', '.text', '.rodata', '.got', '.dynamic', '.plt', '.rela.plt', '.init_array'):
        print("  %-12s addr=%#x off=%#x size=%#x" % (n, s['addr'], s['off'], s['size']))

# .dynsym 解析: 找 Java_ 导出
dynsym = secs[[shname(s['name_off']) for s in secs.values()].index('.dynsym')]
dynstr = secs[[shname(s['name_off']) for s in secs.values()].index('.dynstr')]
dynstr_off = dynstr['off']

ENT = dynsym['entsz'] or 24
for e in range(dynsym['size'] // ENT):
    st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from('<IBBHQQ', d, dynsym['off'] + e * ENT)
    nm = d[dynstr_off + st_name:].split(b'\x00')[0].decode('latin1', 'replace')
    if nm.startswith('Java_') or nm in ('getAesKey', 'getFlexibleSecret', 'base64Encode', 'base64Decode') or 'epay' in nm.lower():
        print("  sym val=%#x size=%#x %s" % (st_value, st_size, nm))

# 保存上下文信息供后续
open(r'C:\Users\20751\Desktop\猫和老鼠\epay_elf_info.txt', 'w').write(
    "machine=0x%x entry=%#x shoff=%#x\n" % (e_machine, e_entry, e_shoff))