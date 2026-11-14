# -*- coding: utf-8 -*-
"""libepay-crypto.so: .rela.dyn 重定位表 -> 找 0xd1138/0xd1148 目标 + dump .data/.data.rel.ro 密钥材料"""
import struct
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()

# .rela.dyn: off 0x2cd68 size 0x10518, 24B/项
RELATIVE = 1027  # R_AARCH64_RELATIVE
print("== .rela.dyn 中 r_offset 命中 0xd10xx-0xd11xx 区间的项 ==")
for i in range(0x10518 // 24):
    r_off, r_info = struct.unpack_from('<QQ', d, 0x2cd68 + i * 24)
    r_type = r_info & 0xffffffff
    r_sym = r_info >> 32
    r_add = struct.unpack_from('<q', d, 0x2cd68 + i * 24 + 16)[0]
    if 0xd1000 <= r_off < 0xd1200:
        print("  r_off=%#x type=%d sym=%d addend=%#x" % (r_off, r_type, r_sym, r_add & 0xffffffffffffffff))

# 也统计所有重定位类型分布
print("\n== 重定位类型分布 ==")
from collections import Counter
c = Counter()
for i in range(0x10518 // 24):
    r_off, r_info = struct.unpack_from('<QQ', d, 0x2cd68 + i * 24)
    c[r_info & 0xffffffff] += 1
for t, n in c.most_common():
    print("  type %d: %d" % (t, n))

# dump .data (VA 0xd1000, off 0xd0000, 0xc8B) 与 .data.rel.ro 部分
print("\n== .data 初始数据 (VA 0xd1000 = off 0xd0000) ==")
chunk = d[0xd0000:0xd0000+0xc8]
print("hex:", chunk.hex())
print("str:", repr(chunk))
# ASCII 可读串
import re
for m in re.finditer(rb'[\x20-\x7e]{4,}', chunk):
    print("  串: %r" % m.group())

print("\n== .got (0xd0068-0xd1000) 中靠近 0xd1000 的尾部 0x40 ==")
tail = d[0xcff00:0xd0000]
print("hex:", tail.hex())