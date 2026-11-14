# -*- coding: utf-8 -*-
"""最后防线: 1) 数据段/方法表对 0xc8b7f8,0xc8c84c,0xc8b838,0xc8c844 的 qword 引用
2) 核实 0xc8a000~0xc8a100 方法表 (0xc8a0b6c/0xc8a0bc4 所在) 内容: 是否含这些 setter
3) 扫描所有 blr 目标间接可达性: 统计 0xc8b7f8 周边 0xb0~0x60 区域是否有指针表
4) 反汇编 0xc8c700~0xc8c7f0 (SSL_CTX_new 尾部/失败清理) 确认无 +0x98 写入"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
CODE_END = 0x10022b8

fns = {0xc8b7f8: 'setter(cmd=0xf->+0x98)', 0xc8c84c: 'set_cert_verify_callback',
       0xc8b838: 'ctrl分发', 0xc8c844: 'set_verify(+0xb0)', 0xc8c83c: 'setter(+0xa8)',
       0xc8c858: 'setter(+0x150/178)', 0xc8c464: 'SSL_CTX_new'}

print("=== 1) 数据段 qword 引用 (代码区外, 含方法表区) ===")
refs = {}
for o in range(0x10022b8, len(d)-8, 8):
    v = struct.unpack_from('<Q', d, o)[0]
    if v in fns:
        refs.setdefault(v, []).append(o)
for v, addrs in refs.items():
    print(f"  {fns[v]}: {len(addrs)} 处")
    for a in addrs[:12]:
        print(f"    [{a:#x}]")

print("\n=== 2) 0xc8a000~0xc8a100 及 0xc8a0b6c/0xc8a0bc4 反汇编 ===")
for ins in md.disasm(d[0xc8a000:0xc8a100], 0xc8a000):
    print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
# 检查 0xc8a0b6c / 0xc8a0bc4 是否代码或数据
for a in (0xc8a0b6c, 0xc8a0bc4, 0xc8a0b00):
    w = struct.unpack_from('<I', d, a)[0]
    print(f"  [{a:#x}] word = {w:#010x}")

print("\n=== 3) 方法表回调查找: SSL_METHOD vtable 内函数指针 (0xc8a000 起前 0x100 解析) ===")
# SSL_METHOD 布局: cb 指针可能指向 setter; 尝试在 0xc8a000~0xc8b000 找 0xc8b7f8/0xc8c84c 的出现
found = []
for off in range(0xc8a000, 0xc8b000, 4):
    w = struct.unpack_from('<I', d, off)[0]
    if w in (0xc8b7f8, 0xc8c84c, 0xc8b838, 0xc8c844):
        found.append((off, hex(w)))
print(f"  0xc8a000~0xc8b000 内出现: {found}")

print("\n=== 4) 0xc8c700~0xc8c7f0 (SSL_CTX_new 尾部) ===")
for ins in md.disasm(d[0xc8c700:0xc8c7f0], 0xc8c700):
    if ins.mnemonic in ('str', 'stp', 'bl', 'b', 'cbnz', 'cbz', 'ret'):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")