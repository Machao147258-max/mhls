# -*- coding: utf-8 -*-
# 扫描 tom_lib 下所有 so 的动态导出符号,找改名后的引擎库(lua/cocos/安全SDK)
import os, re, struct

base = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib'

def elf64_iter(path):
    """yield (name, st_info, st_shndx) for .dynsym entries"""
    data = open(path, 'rb').read()
    if data[:4] != b'\x7fELF':
        return
    is64 = data[4] == 2
    # 节区头表
    e_shoff = struct.unpack_from('<Q', data, 0x28)[0]
    e_shentsize = struct.unpack_from('<H', data, 0x3A)[0]
    e_shnum = struct.unpack_from('<H', data, 0x3C)[0]
    e_shstrndx = struct.unpack_from('<H', data, 0x3E)[0]
    if not e_shoff or not e_shnum:
        return
    # 节名表定位
    shstr_off = e_shoff + e_shstrndx * e_shentsize
    shstr_size = struct.unpack_from('<Q', data, shstr_off + 0x20)[0]
    shstr_addr = struct.unpack_from('<Q', data, shstr_off + 0x18)[0]
    shstr = data[shstr_addr:shstr_addr + shstr_size]
    def secname(i):
        off = struct.unpack_from('<I', data, e_shoff + i * e_shentsize + 0x00)[0]
        end = shstr.find(b'\0', off)
        return shstr[off:end].decode('latin-1')
    dynsym = dynstr = None
    for i in range(e_shnum):
        nm = secname(i)
        if nm == '.dynsym':
            off = struct.unpack_from('<Q', data, e_shoff + i * e_shentsize + 0x18)[0]
            size = struct.unpack_from('<Q', data, e_shoff + i * e_shentsize + 0x20)[0]
            entsz = struct.unpack_from('<Q', data, e_shoff + i * e_shentsize + 0x38)[0] or 24
            dyn_sym = data[off:off + size]
        elif nm == '.dynstr':
            off = struct.unpack_from('<Q', data, e_shoff + i * e_shentsize + 0x18)[0]
            size = struct.unpack_from('<Q', data, e_shoff + i * e_shentsize + 0x20)[0]
            dyn_str = data[off:off + size]
    if dyn_sym is None or dyn_str is None:
        return
    entsz = 24
    for off in range(0, len(dyn_sym), entsz):
        st_name, st_info, st_other, st_shndx = struct.unpack_from('<IBBH', dyn_sym, off)
        if st_name == 0:
            continue
        end = dyn_str.find(b'\0', st_name)
        name = dyn_str[st_name:end].decode('latin-1', 'replace')
        typ = st_info & 0xf
        yield name, typ, st_shndx

def cat(name, typ, shndx):
    # 导出函数 = 已定义 + FUNC;导入 = UND
    if shndx == 0:
        return 'import'
    if typ == 2:
        return 'func'
    if typ == 1:
        return 'object'
    return 'other'

pats = {
    'lua引擎': re.compile(r'^(lua[A-Z_]|luaL_|luaopen_|tolua_|lua_state|lua_State)'),
    'cocos': re.compile(r'^(cocos2d|cocos|CC[A-Z]|CCObject|Director|Sprite)'),
    'xdl': re.compile(r'^xdl'),
    'unisec': re.compile(r'^(unisec|Unitra),|secsdk'),
    'frida检测': re.compile(r'frida|gum|gg_|linjector'),
    '反调试': re.compile(r'ptrace|anti|debug|TracerPid|dumpable'),
    'vm/加固': re.compile(r'vm|pack|protect|shell|加固'),
    'jni': re.compile(r'^Java_'),
    'cpython': re.compile(r'^Py[A-Z]'),
    'unity': re.compile(r'^Unity|mono_'),
}

for f in sorted(os.listdir(base)):
    if not f.endswith('.so'):
        continue
    p = os.path.join(base, f)
    try:
        syms = list(elf64_iter(p))
    except Exception as e:
        print(f, 'ERR', e)
        continue
    if not syms:
        print(f'  (无符号/非ELF)')
        continue
    exports = [(n, t, s) for n, t, s in syms if s != 0]
    imports = [n for n, t, s in syms if s == 0]
    shown = []
    for label, pr in pats.items():
        hits = sorted({n for n, t, s in exports if pr.match(n)})
        if hits:
            shown.append(f'{label}:{len(hits)}')
    # 额外:统计导出函数总数
    nfunc = sum(1 for n, t, s in exports if t == 2)
    line = f'{f:<32} 导出={len(exports):<5} (func {nfunc})  导入={len(imports):<5}'
    if shown:
        line += '  ⚠ ' + ' '.join(shown)
    print(line)
    # lua 引擎命中时打印前几个符号
    for label, pr in pats.items():
        if label == 'lua引擎':
            hits = sorted({n for n, t, s in exports if pr.match(n)})
            if hits:
                print('      lua 样例:', ', '.join(hits[:10]))