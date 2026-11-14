# -*- coding: utf-8 -*-
"""libepay-crypto.so: 解析 .dynsym 索引 449/1541 (GLOB_DAT 符号-> getAesKey 真实现)"""
import struct
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()

# 从节表找 .dynsym/.dynstr/.symtab
e_shoff = struct.unpack_from('<Q', d, 40)[0]
e_shentsize, e_shnum, e_shstrndx = struct.unpack_from('<HHH', d, 58)
secs = []
for i in range(e_shnum):
    off = e_shoff + i * e_shentsize
    sh_name, sh_type, sh_flags, sh_addr, sh_offset, sh_size = struct.unpack_from('<IIQQQQ', d, off)
    secs.append((sh_name, sh_type, sh_addr, sh_offset, sh_size))
shstr = secs[e_shstrndx][3]
names = []
for (sn, st, a, o, sz) in secs:
    z = d.index(b'\x00', shstr + sn)
    names.append(d[shstr+sn:z].decode('latin1'))

dynsym = None; dynstr = None
for i, n in enumerate(names):
    if n == '.dynsym': dynsym = secs[i]
    if n == '.dynstr': dynstr = secs[i]
print(".dynsym:", dynsym, " .dynstr:", dynstr)

ds_off, ds_size = dynsym[3], dynsym[4]   # st_name4 st_info1 st_other1 st_shndx2 st_value8 st_size8 = 24B
dt_off = dynstr[3]

def sym(i):
    o = ds_off + i * 24
    st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from('<IBBHQQ', d, o)
    z = d.index(b'\x00', dt_off + st_name)
    name = d[dt_off+st_name:z].decode('latin1', 'replace')
    return name, st_info, st_shndx, st_value, st_size, o

print("\n== GLOB_DAT 目标符号 ==")
for idx in (449, 1541):
    name, info, shndx, val, size, o = sym(idx)
    print("[%d] %-40s info=%#x shndx=%#x value=%#x size=%#x " % (idx, name, info, shndx, val, size))

# 额外: 打印 .dynsym 中所有定义为函数(STT_FUNC, st_value 在 .text)且名字含 aes/secret/encrypt/decrypt/base64 的符号
print("\n== .dynsym 函数符号 (STT_FUNC/%#x, text区) 关键词过滤 ==")
TEXT_LO, TEXT_HI = 0x408b0, 0xa98ec
import re
cnt = 0
for i in range(ds_size // 24):
    name, info, shndx, val, size, o = sym(i)
    if info >> 4 == 0xf:  # STT_ARM64?? 0xf=STT_GNU_IFUNC; 实际 0x2=STT_FUNC 在低4位
        pass
    typ = info & 0xf
    bind = info >> 4
    if typ == 2 and TEXT_LO <= val < TEXT_HI:
        if re.search(r'aes|secret|encrypt|decrypt|base64|key|md5|sha|hmac|sign', name, re.I) and not name.startswith('.'):
            print("  [%d] %-52s bind=%d type=%d value=%#x size=%#x" % (i, name, bind, typ, val, size))
            cnt += 1
            if cnt > 60: break
print("(共 %d)" % cnt)