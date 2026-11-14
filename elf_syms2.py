# -*- coding: utf-8 -*-
"""解析 ELF 动态符号表: 尝试多种编码解码被混淆的符号名, 查找 SSL/TLS/加密函数地址"""
import struct, sys

LIB = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so"

def parse_elf(path):
    data = open(path, 'rb').read()
    assert data[:4] == b'\x7fELF'
    is64 = data[4] == 2
    endian = '<' if data[5] == 1 else '>'
    if is64:
        e_shoff = struct.unpack_from(endian + 'Q', data, 0x28)[0]
        e_shentsize = struct.unpack_from(endian + 'H', data, 0x3a)[0]
        e_shnum = struct.unpack_from(endian + 'H', data, 0x3c)[0]
        e_shstrndx = struct.unpack_from(endian + 'H', data, 0x3e)[0]
    else:
        e_shoff = struct.unpack_from(endian + 'I', data, 0x20)[0]
        e_shentsize = struct.unpack_from(endian + 'H', data, 0x2e)[0]
        e_shnum = struct.unpack_from(endian + 'H', data, 0x30)[0]
        e_shstrndx = struct.unpack_from(endian + 'H', data, 0x32)[0]
    shdrs = []
    for i in range(e_shnum):
        off = e_shoff + i * e_shentsize
        if is64:
            sh = struct.unpack_from(endian + 'IIQQQQIIQQ', data, off)
            shdrs.append(dict(name=sh[0], type=sh[1], flags=sh[2], addr=sh[3], offset=sh[4], size=sh[5], link=sh[6], info=sh[7], addralign=sh[8], entsize=sh[9]))
        else:
            sh = struct.unpack_from(endian + 'IIIIIIIIII', data, off)
            shdrs.append(dict(name=sh[0], type=sh[1], flags=sh[2], addr=sh[3], offset=sh[4], size=sh[5], link=sh[6], info=sh[7], addralign=sh[8], entsize=sh[9]))
    shstr = shdrs[e_shstrndx]
    shstr_data = data[shstr['offset']:shstr['offset'] + shstr['size']]
    def get_str(tab_off, off):
        tab = data[tab_off:tab_off + 0x100000]
        end = tab.find(b'\x00', off)
        return tab[off:end] if end != -1 else b''
    strtab = None
    for sh in shdrs:
        sname = get_str(shstr['offset'], sh['name']).decode('utf-8', 'replace')
        if sname in ('.dynstr', '.strtab'):
            strtab = sh
            break
    if strtab is None:
        print("no strtab"); return
    # 解码候选: raw / utf-16-le / gbk / latin1 各种变换
    def try_decode(raw):
        out = []
        for enc in ('utf-8', 'gbk', 'latin1', 'utf-16-le', 'utf-16-be'):
            try:
                s = raw.decode(enc)
                out.append(s)
            except Exception:
                pass
        return out
    syms = []
    for sh in shdrs:
        sname = get_str(shstr['offset'], sh['name']).decode('utf-8', 'replace')
        if sname not in ('.dynsym', '.symtab'):
            continue
        entsize = sh['entsize'] or (24 if is64 else 16)
        for off in range(sh['offset'], sh['offset'] + sh['size'], entsize):
            if is64:
                st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from(endian + 'IBBHQQ', data, off)
            else:
                st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack_from(endian + 'IIIBBH', data, off)
            if st_name == 0:
                continue
            raw = get_str(strtab['offset'], st_name)
            if not raw:
                continue
            bind = (st_info >> 4) & 0xf
            typ = st_info & 0xf
            if typ not in (0, 1, 2):
                continue
            if st_value == 0 and typ != 0:
                continue
            syms.append((raw, st_value, st_size, bind, typ, sname))
    return syms

def pat_search(s):
    return any(k in s for k in ("SSL", "ssl", "TLS", "tls", "EVP_", "BIO_", "CRYPTO_", "X509", "encrypt", "decrypt", "cipher", "hmac", "AES", "SHA", "MD5", "RSA"))

syms = parse_elf(LIB)
print("total syms:", len(syms))
hits = []
for raw, value, size, bind, typ, sec in syms:
    decs = try_decode(raw)
    for s in decs:
        if pat_search(s):
            hits.append((s, value, size, bind, typ, raw))
seen = set()
uniq = []
for h in hits:
    if h[0] not in seen:
        seen.add(h[0])
        uniq.append(h)
print("SSL/crypto hits:", len(uniq))
out = r"C:\Users\20751\Desktop\猫和老鼠\ssl_syms_decoded.txt"
with open(out, 'w', encoding='utf-8') as f:
    for s, value, size, bind, typ, raw in sorted(uniq, key=lambda x: x[1]):
        f.write(f"{value:012x} {size:6d} bind={bind} typ={typ} {s}\n")
print("written:", out)