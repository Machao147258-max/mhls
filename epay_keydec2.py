# -*- coding: utf-8 -*-
"""libepay-crypto.so: phdr vaddr->offset 映射 + 解密 0xd10f0 处 26B XOR 密钥材料"""
import struct
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()

# phdr
e_phoff = struct.unpack_from('<Q', d, 32)[0]
e_phentsize, e_phnum = struct.unpack_from('<HH', d, 54)
segs = []
for i in range(e_phnum):
    off = e_phoff + i * e_phentsize
    p_type, p_flags = struct.unpack_from('<II', d, off)
    p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack_from('<QQQQQQ', d, off+8)
    segs.append((p_type, p_offset, p_vaddr, p_filesz, p_memsz))
    if p_type == 1:  # PT_LOAD
        print("LOAD off=%#x vaddr=%#x filesz=%#x memsz=%#x flags=%#x" % (p_offset, p_vaddr, p_filesz, p_memsz, p_flags))

def va2off(va):
    for t, o, v, fsz, msz in segs:
        if t == 1 and v <= va < v + fsz:
            return o + (va - v)
    return None

# 解密: plain[i] = enc[i] ^ key[i%16]
KEY = bytes.fromhex('a35b8f05c98b7dcb')
buf_va = 0xd10f0
bo = va2off(buf_va)
print("\nbuf_va=%#x -> file_off=%s" % (buf_va, hex(bo) if bo else 'None'))
if bo is None:
    print("!! 0xd10f0 不在任何 LOAD 段 filesz 内 (可能 memsz > filesz 的 .bss?)"); raise SystemExit
enc = d[bo:bo+0x1a]
print("密文: %s" % enc.hex())
plain = bytes(enc[i] ^ KEY[i % 16] for i in range(len(enc)))
print("明文: %s" % plain.hex())
print("明文: %r" % plain)

# 同时 dump 该段更多内容, 看相邻是否还有加密表(密钥/IV/盐)
print("\n== 0xd10f0 前 0x40 与后 0x100 解密预览 (含 XOR 全部) ==")
for start in (buf_va - 0x20, buf_va, buf_va + 0x40):
    off = va2off(start)
    if off is None: continue
    chunk = d[off:off+0x60]
    dec = bytes(c ^ KEY[i % 16] for i, c in enumerate(chunk))
    print("VA %#x:" % start)
    print("  raw: %s" % chunk.hex())
    print("  xor: %s  %r" % (dec.hex(), dec))