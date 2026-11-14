# -*- coding: utf-8 -*-
# 从 APK 解出 x86_64 / arm64-v8a 的 so 并扫描动态符号(引擎/安全/反检测)
import os, re, struct, zipfile, sys

APK = sys.argv[1] if len(sys.argv) > 1 else r'C:\Users\20751\Desktop\猫和老鼠\device_base.apk'
OUT = r'C:\Users\20751\Desktop\猫和老鼠\apk_extract'

def syms_from_sections(data):
    """返回 [(name, type, shndx)];None = 无法解析(缺节头/缺dynsym)"""
    if data[:4] != b'\x7fELF':
        return []
    e_shoff = struct.unpack_from('<Q', data, 0x28)[0]
    e_shentsize = struct.unpack_from('<H', data, 0x3A)[0]
    e_shnum = struct.unpack_from('<H', data, 0x3C)[0]
    e_shstrndx = struct.unpack_from('<H', data, 0x3E)[0]
    if not e_shoff or not e_shnum:
        return None
    shstr_off = e_shoff + e_shstrndx * e_shentsize
    shstr_size = struct.unpack_from('<Q', data, shstr_off + 0x20)[0]
    shstr_addr = struct.unpack_from('<Q', data, shstr_off + 0x18)[0]
    shstr = data[shstr_addr:shstr_addr + shstr_size]
    dyn_sym = dyn_str = None
    for i in range(e_shnum):
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
    out = []
    for off in range(0, len(dyn_sym), 24):
        st_name, st_info, st_other, st_shndx = struct.unpack_from('<IBBH', dyn_sym, off)
        if st_name == 0:
            continue
        end = dyn_str.find(b'\0', st_name)
        out.append((dyn_str[st_name:end].decode('latin-1', 'replace'), st_info & 0xf, st_shndx))
    return out

pat_engine = re.compile(r'^(lua[A-Z_0-9]|luaL_|luaopen_|tolua_|cocos2d|cocos|CC[A-Z]|Director|Sprite|spine_)')
pat_sec = re.compile(r'^(unisec|secsdk|sec_lib|sec-lib|WatchPair|tcp_|net_)')
pat_anti = re.compile(r'frida|gum|ptrace|anti.?debug|TracerPid|dumpable', re.IGNORECASE)
LUA_STRS = [b'luaL_loadbuffer', b'lua_getglobal', b'lua_pcall', b'luaL_newstate', b'luaL_loadstring']

z = zipfile.ZipFile(APK)
libs = {}
for n in z.namelist():
    if n.startswith('lib/') and n.endswith('.so'):
        p = n.split('/')
        if len(p) >= 3:
            libs.setdefault(p[1], []).append(n)

print('APK so 分布:', {k: len(v) for k, v in sorted(libs.items())})

def scan_abi(abi):
    print(f'\n===== ABI: {abi} =====')
    for zname in sorted(libs.get(abi, [])):
        fname = zname.rsplit('/', 1)[-1]
        data = z.read(zname)
        syms = syms_from_sections(data)
        if syms is None:
            print(f'{fname:<34} [解析失败/无节头]')
            continue
        exports = [(n, i, s) for n, i, s in syms if s != 0]
        nfunc = sum(1 for n, i, s in exports if i == 2)
        hits = []
        for label, pr in [('lua引擎', pat_engine), ('安全SDK', pat_sec), ('反检测', pat_anti)]:
            h = sorted({n for n, i, s in exports if pr.search(n)})
            if h:
                hits.append(f'{label}:{len(h)}')
        lua_st = sum(data.count(x) for x in LUA_STRS)
        line = f'{fname:<36} 导出={len(exports):<5} (func {nfunc})  lua串={lua_st:<2}'
        if hits:
            line += '  ⚠ ' + ' '.join(hits)
        print(line)
        for label, pr in [('lua引擎', pat_engine), ('反检测', pat_anti)]:
            h = sorted({n for n, i, s in exports if pr.search(n)})
            if h:
                print(f'      [{label}] {", ".join(h[:8])}')

abi = sys.argv[1] if len(sys.argv) > 1 else 'x86_64'
abi = abi if abi in libs else ('x86_64' if 'x86_64' in libs else (sorted(libs.keys()) or [''])[0])
scan_abi(abi)