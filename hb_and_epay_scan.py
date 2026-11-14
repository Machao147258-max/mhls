# -*- coding: utf-8 -*-
"""A) libcocos2dlua.so (1.0.1c) Heartbleed 特征扫描:
   1) 找 ssl3_read_bytes 中 TLS1_RT_HEARTBEAT=0x18 分发点
   2) 找 tls1_process_heartbeat: malloc 长度 = payload+0x13(19=1+2+16padding) 模式
B) libepay-crypto.so 快速侦查: 大小/ELF/敏感字符串"""
import struct, re
from capstone import *

DIR = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib'
MAIN = DIR + r'\libcocos2dlua.so'
EPAY = DIR + r'\libepay-crypto.so'

d = open(MAIN, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True
CODE_END = 0x10022b8

print("=== A1) libcocos2dlua.so: cmp w?, #0x18 (TLS1_RT_HEARTBEAT) 候选点 ===")
hits = []
for lo in range(0, CODE_END, 0x8000):
    hi = min(lo + 0x8000, CODE_END)
    for ins in md.disasm(d[lo:hi], lo):
        if ins.mnemonic == 'cmp' and ins.op_str.endswith('#0x18'):
            hits.append(ins.address)
print(f"  共 {len(hits)} 处; 前 20: {[hex(a) for a in hits[:20]]}")

print("\n=== A2) ssl3_read_bytes 特征: ldrb w?, [x?, #0x100] (rrec.type) 周边找 0x18 分支 ===")
# ssl3_read_bytes 内对 r.data 偏移访问: 先定位含 'cmp' '#0x18' 且附近有 bl 的候选
for a in hits:
    lo = a - 0x40; hi = a + 0x80
    if lo < 0: continue
    seq = []
    for ins in md.disasm(d[lo:hi], lo):
        seq.append((ins.address, ins.mnemonic, ins.op_str))
    # 打印含 a 且周边 0x60 内有 bl 的段
    bls = [s for s in seq if s[1] == 'bl']
    if bls:
        print(f"  --- 0x{a:x} 周边 bl 目标: {[hex(int(s[2][1:],16)) if s[2].startswith('#') else s[2] for s in bls]}")

print("\n=== A3) tls1_process_heartbeat 特征: add x?,x?,#0x13 紧邻 malloc/克隆 ===")
# 找所有 'add' 含 #0x13 (19) 的指令
adds19 = []
for lo in range(0, CODE_END, 0x8000):
    hi = min(lo + 0x8000, CODE_END)
    for ins in md.disasm(d[lo:hi], lo):
        if ins.mnemonic == 'add' and '#0x13' in ins.op_str:
            adds19.append(ins.address)
print(f"  add #0x13 共 {len(adds19)} 处; 前 30: {[hex(a) for a in adds19[:30]]}")

# 对每处 add19, 看后续 0x20 内是否有 bl (malloc) 且之前有 ldrh/ubfx 长度读取
print("\n=== A4) 候选函数级分析: add19 前 0x30 有 n2s 特征(ldrb+orr) 或后 0x20 有 bl ===")
for a in adds19:
    pre = []
    lo = a - 0x30; hi = a + 0x28
    if lo < 0: continue
    seq = list(md.disasm(d[lo:hi], lo))
    ops = ' '.join(f"{s.mnemonic} {s.op_str}" for s in seq)
    bl_after = any(s.mnemonic == 'bl' and s.address > a for s in seq)
    if ('ldrb' in ops and ('orr' in ops or 'lsl' in ops)) or bl_after:
        print(f"  0x{a:x}: pre/post 含 ldrb/orr 或 bl → {ops[:160]}")

print("\n=== B) libepay-crypto.so 侦查 ===")
try:
    ep = open(EPAY, 'rb').read()
    print(f"  大小: {len(ep)} ({hex(len(ep))})")
    if len(ep) > 0x40 and ep[:4] == b'\x7fELF':
        print("  ELF magic OK, class:", 'ELF64' if ep[4] == 2 else 'ELF32', "machine:", hex(struct.unpack_from('<H', ep, 18)[0]))
        # 敏感字符串
        strs = re.findall(rb'[\x20-\x7e]{6,}', ep)
        keys = ['OpenSSL', 'xxtea', 'AES', 'RSA', 'DES', 'secret', 'password', 'key', 'crypt',
                'netease', 'private', 'BEGIN', 'MD5', 'SHA', 'HMAC', 'base64', 'TEA', 'crc', 'zlib']
        print("  命中关键词串:")
        seen = set()
        for s in strs:
            for k in keys:
                if k.encode() in s.lower() and s not in seen:
                    seen.add(s)
                    print(f"    {s[:100].decode('latin1')}")
                    break
    else:
        print("  非 ELF, 前16字节:", ep[:16])
except FileNotFoundError:
    print("  libepay-crypto.so 不存在")