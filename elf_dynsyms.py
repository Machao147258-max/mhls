# -*- coding: utf-8 -*-
"""从 ELF 的 PT_DYNAMIC 段解析动态符号表(绕过被剥离的 section header)"""
import struct, sys

LIB = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so"

def parse_phdrs(data):
    is64 = data[4] == 2
    endian = '<' if data[5] == 1 else '>'
    if is64:
        e_phoff = struct.unpack_from(endian + 'Q', data, 0x20)[0]
        e_phentsize = struct.unpack_from(endian + 'H', data, 0x36)[0]
        e_phnum = struct.unpack_from(endian + 'H', data, 0x38)[0]
    else:
        e_phoff = struct.unpack_from(endian + 'I', data, 0x1c)[0]
        e_phentsize = struct.unpack_from(endian + 'H', data, 0x2a)[0]
        e_phnum = struct.unpack_from(endian + 'H', data, 0x2c)[0]
    phdrs = []
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        if is64:
            p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack_from(endian + 'IIQQQQQQ', data, off)
        else:
            p_type, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_flags, p_align = struct.unpack_from(endian + 'IIIIIIII', data, off)
        phdrs.append(dict(type=p_type, flags=p_flags, offset=p_offset, vaddr=p_vaddr, filesz=p_filesz, memsz=p_memsz))
    return phdrs, endian, is64

def get_dynamic(data):
    phdrs, endian, is64 = parse_phdrs(data)
    dyn = None
    for ph in phdrs:
        if ph['type'] == 2:  # PT_DYNAMIC
            dyn = ph
            break
    if dyn is None:
        print("no PT_DYNAMIC"); return None
    off = dyn['offset']
    sz = dyn['filesz']
    entries = {}
    if is64:
        for i in range(0, sz - 16, 16):
            tag, val = struct.unpack_from(endian + 'qQ', data, off + i)
            entries[tag] = val
    else:
        for i in range(0, sz - 8, 8):
            tag, val = struct.unpack_from(endian + 'iI', data, off + i)
            entries[tag] = val
    return entries

def vaddr_to_offset(data, vaddr):
    phdrs, endian, is64 = parse_phdrs(data)
    for ph in phdrs:
        if ph['type'] == 1 and ph['vaddr'] <= vaddr < ph['vaddr'] + min(ph['filesz'], ph['memsz']):
            return ph['offset'] + (vaddr - ph['vaddr'])
    return None

def main():
    data = open(LIB, 'rb').read()
    entries = get_dynamic(data)
    if entries is None:
        return
    DT_SYMTAB, DT_STRTAB, DT_SYMENT, DT_STRSZ = 6, 5, 11, 10
    symtab_v = entries.get(DT_SYMTAB)
    strtab_v = entries.get(DT_STRTAB)
    syment = entries.get(DT_SYMENT, 24)
    print(f"symtab@{symtab_v:#x} strtab@{strtab_v:#x} syment={syment}")
    symtab_off = vaddr_to_offset(data, symtab_v)
    strtab_off = vaddr_to_offset(data, strtab_v)
    print(f"file offsets: symtab={symtab_off:#x} strtab={strtab_off:#x}")
    # 估算符号数量: 从 symtab_off 到 strtab 之间
    max_est = (strtab_off - symtab_off) // syment if strtab_off and symtab_off else 200000
    n = min(max_est, 300000)
    endian = '<'
    pats = (b'SSL', b'ssl_', b'SSL_', b'tls', b'TLS', b'EVP_', b'BIO_', b'CRYPTO_', b'X509', b'encrypt', b'decrypt', b'AES_', b'SHA', b'MD5', b'RSA_', b'hmac', b'ngssl', b'mmtls')
    hits = []
    for i in range(n):
        o = symtab_off + i * syment
        if o + 24 > len(data):
            break
        st_name, st_info, st_other, st_shndx, st_value, st_size = struct.unpack_from('<IBBHQQ', data, o)
        if st_name == 0:
            continue
        if st_name > 0x400000:
            continue
        # 读取名字
        if st_name >= len(data) - strtab_off:
            continue
        name_start = strtab_off + st_name
        end = data.find(b'\x00', name_start)
        raw = data[name_start:end]
        if not raw:
            continue
        # 解码尝试
        dec = None
        for enc in ('utf-8', 'ascii'):
            try:
                dec = raw.decode(enc)
                break
            except Exception:
                pass
        if dec is None:
            continue
        bind = (st_info >> 4) & 0xf
        typ = st_info & 0xf
        if any(p in raw for p in pats):
            hits.append((dec, st_value, st_size, bind, typ))
    print("== SSL/crypto hits (dynsym) ==")
    out = open(r"C:\Users\20751\Desktop\猫和老鼠\ssl_syms_dyn.txt", 'w', encoding='utf-8')
    for dec, st_value, st_size, bind, typ in sorted(hits, key=lambda x: x[1]):
        line = f"{st_value:012x} {st_size:6d} bind={bind} typ={typ} {dec}"
        print(line)
        out.write(line + "\n")
    out.close()
    print("total:", len(hits))

main()