# -*- coding: utf-8 -*-
"""1) 反汇编 0x8dcf80~0x8dd600 (含 SSL_CTX_set_verify 调用点的函数体)
2) 反汇编 0x1760890 / 0x17c4718 指针表周边, 找到引用它们的代码(间接调用点)
3) 扫描所有 blr/ldr 使用 0x1760890 槽的代码"""
import struct
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.skipdata = True
CODE_END = 0x10022b8

def dis(lo, hi, tag):
    print(f"\n=== {tag} ({lo:#x}~{hi:#x}) ===")
    cnt = 0
    for ins in md.disasm(d[lo:hi], lo):
        print(f"  {ins.address:#x}: {ins.mnemonic:8s} {ins.op_str}")
        cnt += 1
        if cnt > 260: 
            print("  ... (truncated)")
            break

print("=== 1) 0x8dcf80~0x8dd600 函数体 ===")
dis(0x8dcf80, 0x8dd600, 'SSL_CTX 配置函数')

print("\n=== 2) 指针表周边 ===")
for base in (0x1760890, 0x17c4718, 0x177e5c0):
    print(f"  --- {base:#x} 周边 ---")
    for k in range(-2, 3):
        a = base + k*8
        v = struct.unpack_from('<Q', d, a)[0]
        print(f"    [{a:#x}] = {v:#x} ({'code' if v < CODE_END else 'data'})")

print("\n=== 3) blr 通过 GOT 槽间接调用 ===")
# 槽: 0x1760890(SSL_CTX_set_verify), 0x1760898(下一项), 0x17c4718(SSL_CTX_set_cert_verify_callback)
# 找代码区 ldr x?, [x?, #imm] 其中 x?+imm == 槽地址
slots = {0x1760890: 'SSL_CTX_set_verify', 0x17c4718: 'SSL_CTX_set_cert_verify_callback',
         0x186bf80: 'SSL_CTX_set_cert_verify_callback(b)', 0x177e5c0: 'setter@0xa8'}
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0xFFC00000) == 0xF9400000:  # ldr xRt, [xRn, #imm]
        imm = ((w >> 10) & 0xFFF) << 3
        rn = (w >> 5) & 0x1F
        rt = w & 0x1F
        if imm == 0:
            continue
        # 无法直接知道 rn 值, 跳过; 改用页级搜索
print("(ldr 动态基址无法静态解析, 改为搜索前序 adrp 到对应页)")

# 页: 0x1760000 / 0x17c4000 / 0x186b000 / 0x186b000
pagemap = {0x1760000: '0x1760890 page', 0x17c4000: '0x17c4718 page', 0x186b000: '0x186bf80 page'}
hits = []
for o in range(0, CODE_END-4, 4):
    w = struct.unpack_from('<I', d, o)[0]
    if (w & 0x9F000000) == 0x90000000:
        immhi = (w >> 5) & 0x7FFFF
        immlo = (w >> 29) & 0x3
        imm = (immhi << 14) | (immlo << 12)
        if imm & 0x100000: imm -= 0x200000
        page = ((o >> 12) << 12) + imm
        if page in pagemap:
            hits.append((o, pagemap[page]))
print(f"\n  引用 {pagemap} 的 adrp: {len(hits)} 处")
seen = set()
for h, tag in hits[:40]:
    if h in seen: continue
    seen.add(h)
    print(f"    {h:#x} ({tag})")
    # 后两条指令
    for k in range(1, 3):
        nxt = struct.unpack_from('<I', d, h+4*k)[0]
        print(f"      +{k}: {nxt:#010x}")