# -*- coding: utf-8 -*-
"""find_undump.py — 在 stripped 引擎库中定位引用 luac 魔数的代码(luaU_undump)"""
import struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
MAGIC_FILE_OFF = 0xd55fa0

d = open(SO, 'rb').read()

# 1. ELF 段表: vaddr <-> file offset
assert d[:4] == b'\x7fELF'
e_phoff = struct.unpack_from('<Q', d, 0x20)[0]
e_phentsize = struct.unpack_from('<H', d, 0x36)[0]
e_phnum = struct.unpack_from('<H', d, 0x38)[0]
segs = []
for i in range(e_phnum):
    o = e_phoff + i * e_phentsize
    p_type = struct.unpack_from('<I', d, o)[0]
    p_offset = struct.unpack_from('<Q', d, o + 0x08)[0]
    p_vaddr = struct.unpack_from('<Q', d, o + 0x10)[0]
    p_filesz = struct.unpack_from('<Q', d, o + 0x20)[0]
    segs.append((p_type, p_offset, p_vaddr, p_filesz))

def off2va(off):
    for t, po, pv, pz in segs:
        if po <= off < po + pz:
            return pv + (off - po)
    return None

def va2off(va):
    for t, po, pv, pz in segs:
        if pv <= va < pv + pz:
            return po + (va - pv)
    return None

magic_va = off2va(MAGIC_FILE_OFF)
print('魔数 vaddr: %#x' % magic_va)

# 2. 定位 .text
text = None
for t, po, pv, pz in segs:
    if t == 1 and pz > 5 * 1024 * 1024:  # PT_LOAD, 大段 = 含 .text
        text = (po, pv, pz)
print('text 段: file %#x va %#x size %#x' % text)
t_po, t_va, t_sz = text
code = d[t_po:t_po + t_sz]

# 3. 反汇编找 ADRP 引用魔数页
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True
magic_page = magic_va & ~0xFFF
hits = []
for ins in md.disasm(code, t_va):
    if ins.mnemonic == 'adrp':
        # 提取 adrp 目标: x86-64 capstone 对 arm64 的 adrp 有 operands[0].imm
        try:
            tgt = ins.operands[1].imm
        except Exception:
            tgt = None
        if tgt is not None and (tgt & ~0xFFF) == magic_page:
            hits.append(ins.address)
print('引用魔数页的 ADRP 数量:', len(hits))
for a in hits[:10]:
    print('  ADRP @ %#x' % a)

# 4. 对每个 ADRP,反汇编其后的指令窗口,找 ADD 形成完整地址
for a in hits[:3]:
    start = a - 64
    print('\n=== 窗口 @ %#x (函数区) ===' % a)
    for ins in md.disasm(code[start - t_va:start - t_va + 256], start):
        show = ins.address - a
        extra = ''
        if ins.mnemonic == 'adrp':
            try:
                extra = '  -> page %#x' % ins.operands[1].imm
            except Exception:
                pass
        print('  %+5d  %#x: %s %s' % (show, ins.address, ins.mnemonic, ins.op_str + extra))