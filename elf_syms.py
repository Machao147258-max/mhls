# -*- coding: utf-8 -*-
"""解析 ELF .dynsym, 提取所有与 SSL/TLS/加密相关的导出符号 名称->地址"""
import struct, sys, os

LIB = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so"
PATTERNS = ["SSL", "ssl", "TLS", "tls", "EVP_", "BIO_", "CRYPTO_", "RSA", "AES", "SHA", "MD5", "encrypt", "decrypt", "cipher", "crypto", "X509", "PEM", "ngssl", "mmtls", "nls", "handshake"]

def parse_elf(path):
    data = open(path, 'rb').read()
    if data[:4] != b'\x7fELF':
        print("not ELF"); return
    is64 = data[4] == 2
    little = data[5] == 1
    endian = '<' if little else '>'
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
    # section string table
    shstr = shdrs[e_shstrndx]
    shstr_data = data[shstr['offset']:shstr['offset'] + shstr['size']]
    def get_str(tab, off):
        end = tab.find(b'\x00', off)
        return tab[off:end].decode('utf-8', 'replace') if end != -1 else ''
    for sh in shdrs:
        sname = get_str(shstr_data, sh['name'])
        if sname in ('.dynsym', '.symtab'):
            entsize = sh['entsize'] or (24 if is64 else 16)
            syms = []
            for off in range(sh['offset'], sh['offset'] + sh['size'], entsize):
                if is64:
                    st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from(endian + 'IBBHQQ', data, off)
                else:
                    st_name, st_value, st_size, st_info, st_other, st_shndx = struct.unpack_from(endian + 'IIIBBH', data, off)
                if st_name == 0:
                    continue
                name = get_str(data[shdrs[sh['link']]['offset']:shdrs[sh['link']]['offset'] + shdrs[sh['link']]['size']], st_name) if sh['link'] < len(shdrs) else ''
                bind = (st_info >> 4) & 0xf
                typ = st_info & 0xf
                if any(p.lower() in name.lower() for p in PATTERNS):
                    syms.append((name, st_value, st_size, bind, typ))
            print(f"== {sname}: {len(syms)} matches ==")
            for name, addr, size, bind, typ in sorted(syms, key=lambda x: x[1]):
                b = {0:'LOCAL',1:'GLOBAL',2:'WEAK'}.get(bind, str(bind))
                t = {0:'NOTYPE',1:'OBJECT',2:'FUNC',3:'SECTION'}.get(typ, str(typ))
                if addr != 0 and typ in (1, 2):
                    print(f"{addr:012x} {size:6d} {b:6s} {t:6s} {name}")

parse_elf(LIB)