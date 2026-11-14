# -*- coding: utf-8 -*-
"""修复版: 全 text 段 BL/AAdr xref + 证书 pin 数据搜索 (libAudioCommon.so)"""
import struct, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so"
data = open(SO, 'rb').read()

# ELF64 PHDR
def load_segments(data):
    e_phoff = struct.unpack_from('<Q', data, 32)[0]
    e_phentsize = struct.unpack_from('<H', data, 54)[0]
    e_phnum = struct.unpack_from('<H', data, 56)[0]
    fmt = '<IIQQQQQQ'
    segs = []
    for i in range(e_phnum):
        off = e_phoff + i * e_phentsize
        p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack_from(fmt, data, off)
        if p_type == 1:
            segs.append((p_vaddr, p_offset, p_filesz, p_flags))
    return segs

segs = load_segments(data)
# text 段 = 可执行 PT_LOAD 中范围最大的
exec_segs = [s for s in segs if s[3] & 1]
text_seg = max(exec_segs, key=lambda s: s[2])
tv, to, tsz, tf = text_seg
print(f"text seg: vaddr=0x{tv:x} off=0x{to:x} size=0x{tsz:x} flags={tf}")

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# ---- XREF: 谁 BL 到这些 SSL 校验/配置函数 ----
targets = {
    0x21bba8: "SSL_CTX_set_verify",
    0x21bba0: "SSL_CTX_set_cert_verify_callback",
    0x2a2dd4: "X509_verify_cert",
    0x212894: "ssl_verify_cert_chain",
    0x22b450: "tls_process_server_certificate",
    0x22cdec: "ssl3_check_cert_and_algorithm",
    0x21ca68: "SSL_get_verify_result",
    0x2a09e4: "X509_STORE_add_cert",
    0x21b7a8: "SSL_CTX_new",
    0x217634: "SSL_new",
    0x21c9a0: "SSL_CTX_set_default_verify_paths",
    0x21ca58: "SSL_CTX_load_verify_locations",
}
print("\n===== BL xref =====")
code = data[to:to+tsz]
bl_hits = {}
for ins in md.disasm(code, tv):
    if ins.mnemonic == 'bl':
        tgt = ins.operands[0].imm if ins.operands else None
        if tgt in targets:
            bl_hits.setdefault(targets[tgt], []).append(ins.address)
for name, addrs in sorted(bl_hits.items()):
    print(f"  {name:42s} <- {', '.join(hex(a) for a in addrs[:12])}")

# ---- ADRP+LDR (GOT/全局) 引用 -- 找数据引用(回调/变量) ----
print("\n===== ADRP/ADD refs (to target addr) =====")
adrp_refs = {}
for ins in md.disasm(code, tv):
    if ins.mnemonic == 'adrp':
        tgt_page = ins.operands[0].imm
        ins2 = None
        # 简化: 记录 adrp 目标页, 下一指令通常是 add/ldr
        adrp_refs[ins.address] = tgt_page
for ins in md.disasm(code, tv):
    if ins.mnemonic in ('add', 'ldr', 'ldur') and ins.address-4 in adrp_refs:
        page = adrp_refs[ins.address-4]
        base_reg = ins.operands[0].type
        rm = ins.operands[2] if len(ins.operands) > 2 else None
        if rm and rm.type == 3:  # imm
            full = page + rm.imm
            if full in targets:
                print(f"  {targets[full]:42s} <- data-ref @ 0x{ins.address-4:x} (adrp) + 0x{ins.address:x}")
                # 记录引用所在函数(向前找最近的 stp/prologue 不易, 仅打印)

# ---- 证书 pin 数据搜索 ----
print("\n===== Pin / 证书数据搜索 =====")
pats = {
    "BEGIN CERTIFICATE": rb"-----BEGIN CERTIFICATE-----",
    "BEGIN PUBLIC KEY": rb"-----BEGIN PUBLIC KEY-----",
    "BEGIN RSA PUBLIC KEY": rb"-----BEGIN RSA PUBLIC KEY-----",
    "sha256 hex (64b)": rb"[0-9a-fA-F]{64}",
    "base64 44 (32B)": rb"[A-Za-z0-9+/]{44}=",
}
for name, pat in pats.items():
    if name == "sha256 hex (64b)":
        ms = re.findall(pat, data)
        # 从 .rodata 区域(文件偏移>text 后) 找, 过滤非可打印上下文
        uniq = []
        for m in ms:
            if 0x300000 < data.find(m) < len(data):
                uniq.append(m)
        print(f"  {name}: {len(uniq)} (uniq)")
        for u in uniq[:8]:
            off = data.find(u)
            print(f"    0x{off:x}: {u.decode()[:70]}")
    elif name == "base64 44 (32B)":
        ms = re.findall(pat, data)
        print(f"  {name}: {len(ms)}")
        for m in ms[:10]:
            off = data.find(m)
            print(f"    0x{off:x}: {m.decode()[:50]}")
    else:
        cnt = data.count(pat)
        if cnt:
            off = data.find(pat)
            print(f"  {name}: {cnt} @ first 0x{off:x}")
            print(f"    ctx: {data[off:off+90]}")
        else:
            print(f"  {name}: 0")