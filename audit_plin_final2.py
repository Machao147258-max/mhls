# -*- coding: utf-8 -*-
"""分片版: 扫描代码区所有 adrp 目标页 + 数据表核查"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
CODE_END = 0x10022b8

fns = {0xc8b7f8: 'cmd0xf->+0x98', 0xc8c84c: 'set_cert_verify_callback',
       0xc8b838: 'ctrl分发', 0xc8c844: 'set_verify(+0xb0)', 0xc8c83c: 'setter(+0xa8)',
       0xc8c858: 'setter(+0x150/178)', 0xc8c464: 'SSL_CTX_new'}

print("=== 1) 数据段 qword 引用 (代码区外) ===")
refs = {}
for o in range(CODE_END, len(d)-8, 8):
    v = struct.unpack_from('<Q', d, o)[0]
    if v in fns:
        refs.setdefault(v, []).append(o)
pages = {}
for v, addrs in refs.items():
    print(f"  {fns[v]}: {len(addrs)} 处 {[hex(a) for a in addrs]}")
    for a in addrs:
        pages.setdefault((a >> 12) << 12, set()).add(v)

print("\n=== 2) 代码区 adrp 对这些数据页的引用 (分片 0x8000 字节) ===")
adrp_targets = set()
CH = 0x8000
for lo in range(0, CODE_END, CH):
    hi = min(lo + CH, CODE_END)
    for ins in md.disasm(d[lo:hi], lo):
        if ins.mnemonic == 'adrp':
            b = (ins.bytes[3] << 24) | (ins.bytes[2] << 16) | (ins.bytes[1] << 8) | ins.bytes[0]
            immhi = (b >> 5) & 0x7ffff
            immlo = (b >> 29) & 0x3
            imm = (immhi << 14) | (immlo << 12)
            if imm & 0x100000:
                imm -= 0x200000
            pc_page = ins.address & ~0xfff
            adrp_targets.add((pc_page + imm) & 0xfffffffffffff000)
print(f"  adrp 目标页总数: {len(adrp_targets)}")
hit = False
for page, vs in sorted(pages.items()):
    hitp = page in adrp_targets
    if hitp:
        hit = True
    print(f"  page {page:#x} 含 {[fns[v] for v in vs]}: adrp引用 {'YES!!' if hitp else '无'}")
if not hit:
    print("  => 全部数据表页均无代码 adrp 引用 (死数据/导出元数据, 无 blr 间接路径)")

print("\n=== 3) 0xc8ab00~0xc8ac00 反汇编 (SSL_CTX_new 读取的方法表区) ===")
for ins in md.disasm(d[0xc8ab00:0xc8ac00], 0xc8ab00):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
print("--- 按 qword 指针读 0xc8ab60~0xc8abc0 ---")
for a in range(0xc8ab60, 0xc8abc0, 8):
    v = struct.unpack_from('<Q', d, a)[0]
    if 0x0 < v < CODE_END:
        print(f"  [{a:#x}] -> code {v:#x}")
    else:
        print(f"  [{a:#x}] -> {v:#x}")

print("\n=== 4) 数据段表周边 0x40 字节窗口内容 ===")
for base in (0x17e5520, 0x1887ac0, 0x17c4718, 0x186bf80):
    print(f"  --- {base:#x} ---")
    for o in range(base-0x28, base+0x30, 8):
        v = struct.unpack_from('<Q', d, o)[0]
        mark = ' <==' if o == base else ''
        print(f"    [{o:#x}] {v:#x}{mark}")