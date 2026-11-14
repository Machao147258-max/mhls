# -*- coding: utf-8 -*-
"""arm64 反汇编 + BL xref 分析 libAudioCommon.so (静态破 SSL 核心)"""
import struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so"
data = open(SO, 'rb').read()

# ---- ELF64 PHDR 解析: vaddr -> file offset ----
def load_segments(data):
    if data[:4] != b'\x7fELF':
        raise SystemExit("not ELF")
    is64 = data[4] == 2
    little = data[5] == 1
    endian = '<' if little else '>'
    if is64:
        e_phoff = struct.unpack_from(endian + 'Q', data, 32)[0]
        e_phentsize = struct.unpack_from(endian + 'H', data, 54)[0]
        e_phnum = struct.unpack_from(endian + 'H', data, 56)[0]
        fmt = endian + 'IIQQQQQQ'
        segs = []
        for i in range(e_phnum):
            off = e_phoff + i * e_phentsize
            p_type, p_flags, p_offset, p_vaddr, p_paddr, p_filesz, p_memsz, p_align = struct.unpack_from(fmt, data, off)
            if p_type == 1:  # PT_LOAD
                segs.append((p_vaddr, p_offset, p_filesz))
        return segs
    raise SystemExit("32bit unsupported")

segs = load_segments(data)

def v2o(vaddr):
    for v, o, sz in segs:
        if v <= vaddr < v + sz:
            return o + (vaddr - v)
    return None

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

def disas(vaddr, size, maxlines=200):
    off = v2o(vaddr)
    if off is None:
        print(f"  [v2o fail 0x{vaddr:x}]")
        return []
    code = data[off:off+size]
    out = []
    for ins in md.disasm(code, vaddr):
        out.append(ins)
        if len(out) >= maxlines:
            break
    return out

# 1) 反汇编核心校验函数
for name, vaddr, size in [
    ("X509_verify_cert", 0x2a2dd4, 868),
    ("ssl_verify_cert_chain", 0x212894, 584),
    ("tls_process_server_certificate", 0x22b450, 1204),
    ("ssl3_check_cert_and_algorithm", 0x22cdec, 240),
]:
    print(f"\n========== {name} @ 0x{vaddr:x} ==========")
    for ins in disas(vaddr, size, 250):
        print(f"  0x{ins.address:x}: {ins.mnemonic:10s} {ins.op_str}")

# 2) 全段扫描 BL 引用到 set_verify / set_cert_verify_callback / X509_verify_cert
print("\n========== XREF scan ==========")
targets = {
    0x21bba8: "SSL_CTX_set_verify",
    0x21bba0: "SSL_CTX_set_cert_verify_callback",
    0x2a2dd4: "X509_verify_cert",
    0x212894: "ssl_verify_cert_chain",
    0x22b450: "tls_process_server_certificate",
    0x22cdec: "ssl3_check_cert_and_algorithm",
    0x21ca68: "SSL_get_verify_result",
    0x2a09e4: "X509_STORE_add_cert",
}
# 找到 text 段范围
text_seg = None
for v, o, sz in segs:
    if 0x200000 <= v < 0x300000 or (0x200000 <= v and sz > 0x100000):
        text_seg = (v, o, sz)
        break
print("text seg:", text_seg)
tv, to, tsz = text_seg
code = data[to:to+tsz]
for ins in md.disasm(code, tv):
    if ins.mnemonic == 'bl':
        tgt = ins.operands[0].imm if ins.operands else None
        if tgt in targets:
            print(f"  BL {targets[tgt]}  <- caller @ 0x{ins.address:x}")