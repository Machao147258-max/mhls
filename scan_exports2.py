# -*- coding: utf-8 -*-
# 深挖:1) libcocos2dlua/libunisec 为什么解析不了(ELF头 + PT_DYNAMIC 兜底)
#      2) 全库 loose 搜 lua/cocos/tolua 导出符号
import os, struct

base = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib'

def parse_elf(path):
    data = open(path, 'rb').read()
    if data[:4] != b'\x7fELF':
        return None
    e_shoff = struct.unpack_from('<Q', data, 0x28)[0]
    e_phoff = struct.unpack_from('<Q', data, 0x20)[0]
    e_phentsize = struct.unpack_from('<H', data, 0x36)[0]
    e_phnum = struct.unpack_from('<H', data, 0x38)[0]
    e_shnum = struct.unpack_from('<H', data, 0x3C)[0]
    e_shstrndx = struct.unpack_from('<H', data, 0x3E)[0]
    e_machine = struct.unpack_from('<H', data, 0x12)[0]
    return dict(data=data, shoff=e_shoff, phoff=e_phoff, phentsz=e_phentsize,
                phnum=e_phnum, shnum=e_shnum, shstrndx=e_shstrndx, machine=e_machine)

def syms_from_sections(h):
    """从节头表读 .dynsym/.dynstr"""
    data = h['data']
    e_shoff, e_shentsize = h['shoff'], 0x40
    shstr_off = e_shoff + h['shstrndx'] * e_shentsize
    shstr_size = struct.unpack_from('<Q', data, shstr_off + 0x20)[0]
    shstr_addr = struct.unpack_from('<Q', data, shstr_off + 0x18)[0]
    shstr = data[shstr_addr:shstr_addr + shstr_size]
    dyn_sym = dyn_str = None
    for i in range(h['shnum']):
        o = e_shoff + i * e_shentsize
        noff = struct.unpack_from('<I', data, o)[0]
        nm = shstr[noff:shstr.find(b'\0', noff)].decode('latin-1')
        if nm == '.dynsym':
            off = struct.unpack_from('<Q', data, o + 0x18)[0]
            size = struct.unpack_from('<Q', data, o + 0x20)[0]
            dyn_sym = data[off:off + size]
        elif nm == '.dynstr':
            off = struct.unpack_from('<Q', data, o + 0x18)[0]
            size = struct.unpack_from('<Q', data, o + 0x20)[0]
            dyn_str = data[off:off + size]
    if dyn_sym is None:
        return None
    for off in range(0, len(dyn_sym), 24):
        st_name, st_info, st_other, st_shndx = struct.unpack_from('<IBBH', dyn_sym, off)
        if st_name == 0:
            continue
        end = dyn_str.find(b'\0', st_name)
        yield dyn_str[st_name:end].decode('latin-1', 'replace'), st_info & 0xf, st_shndx

def syms_from_dynamic(h):
    """stripped: PT_DYNAMIC → DT_SYMTAB/DT_STRTAB,符号数走 DT_HASH/GNU_HASH"""
    data = h['data']
    base_va = base_off = None
    dyn_va = dyn_sz = None
    for i in range(h['phnum']):
        o = h['phoff'] + i * h['phentsz']
        p_type, = struct.unpack_from('<I', data, o)
        if p_type == 1:  # PT_LOAD
            if base_va is None:
                base_va = struct.unpack_from('<Q', data, o + 0x10)[0]
                base_off = struct.unpack_from('<Q', data, o + 0x08)[0]
        elif p_type == 2:  # PT_DYNAMIC
            dyn_va = struct.unpack_from('<Q', data, o + 0x10)[0]
            dyn_sz = struct.unpack_from('<Q', data, o + 0x20)[0]
    if dyn_va is None or base_va is None:
        return None
    def va2off(va):
        return va - base_va + base_off
    tags = {}
    for o in range(va2off(dyn_va), va2off(dyn_va) + dyn_sz, 16):
        t, v = struct.unpack_from('<QQ', data, o)
        tags[t] = v
    symtab = tags.get(6)
    strtab = tags.get(5)
    if symtab is None or strtab is None:
        return None
    n = 65536
    if 4 in tags:  # DT_HASH
        ho = va2off(tags[4])
        n = struct.unpack_from('<I', data, ho + 4)[0]  # nchain
    elif 0x6ffffef5 in tags:  # DT_GNU_HASH
        ho = va2off(tags[0x6ffffef5])
        nbucket, symoffset, bloom_sz, = struct.unpack_from('<III', data, ho)
        b_off = ho + 16 + bloom_sz * 8
        maxi = symoffset
        for i in range(nbucket):
            b, = struct.unpack_from('<I', data, b_off + i * 4)
            maxi = max(maxi, b)
        idx = maxi
        c_off = b_off + nbucket * 4
        while True:
            c, = struct.unpack_from('<I', data, c_off + (idx - symoffset) * 4)
            idx += 1
            if c & 1:
                break
        n = idx
    sym_off = va2off(symtab)
    try:
        str_sz = data.find(b'\0', va2off(strtab)) - va2off(strtab)
    except Exception:
        return None
    str_bytes = data[va2off(strtab):va2off(strtab) + str_sz]
    for i in range(1, n):
        o = st_off = symtab_off = 0
        o = sym_off + i * 24
        st_name, st_info, st_other, st_shndx = struct.unpack_from('<IBBH', data, o)
        if st_name == 0:
            continue
        end = str_bytes.find(b'\0', st_name)
        yield str_bytes[st_name:end].decode('latin-1', 'replace'), st_info & 0xf, st_shndx

print('=== 1) stripped 嫌疑库 ===')
for f in ['libcocos2dlua.so', 'libunisec.so']:
    h = parse_elf(os.path.join(base, f))
    if not h:
        print(f, '非ELF'); continue
    secs = list(syms_from_sections(h)) if h['shoff'] else None
    if secs is None:
        print(f'{f:<18} 无节头表(e_shoff=0),尝试 PT_DYNAMIC…')
        secs = list(syms_from_dynamic(h)) if h else None
    if not secs:
        print(f'{f:<18} 仍无符号 — 高度 stripped')
        continue
    ex = [s for s in secs if s[2] != 0]
    im = [s for s in secs if s[2] == 0]
    print(f'{f:<18} 导出={len(ex)} 导入={len(im)}')
    for pat in ['lua', 'cocos', 'tolua']:
        hits = sorted({n for n, i, s in ex if pat in n.lower()})
        if hits:
            print(f'   [{pat}] {len(hits)}: {", ".join(hits[:10])}')

print()
print('=== 2. 全库 loose 搜 lua/cocos/tolua 导出 ===')
for f in sorted(os.listdir(base)):
    if not f.endswith('.so'):
        continue
    h = parse_elf(os.path.join(base, f))
    if not h:
        continue
    secs = syms_from_sections(h)
    if secs is None and h['shnum'] == 0:
        secs = syms_from_dynamic(h)
    if not secs:
        continue
    ex = [s for s in secs if s[2] != 0]
    if not ex:
        continue
    for pat in ['lua', 'cocos', 'tolua', 'xdl', 'anti']:
        hits = sorted({n for n, i, s in ex if pat in n.lower()})
        if hits:
            shown = ", ".join(hits[:6]) + (', …' if len(hits) > 6 else '')
            print(f'{f:<26} [{pat}] {len(hits):>4}: {shown}')