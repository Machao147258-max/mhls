# -*- coding: utf-8 -*-
"""修正: 选含目标函数地址的 exec 段做全量 BL xref + curl 版本确认 + pin 搜索"""
import struct, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so"
data = open(SO, 'rb').read()

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
print("=== PT_LOAD segments ===")
for v, o, sz, fl in segs:
    print(f"  vaddr=0x{v:x} off=0x{o:x} size=0x{sz:x} flags={fl}")

# 选包含 0x22b450 (tls_process_server_certificate) 的段
def seg_of(vaddr):
    for v, o, sz, fl in segs:
        if v <= vaddr < v + sz:
            return (v, o, sz, fl)
    return None

text_seg = seg_of(0x22b450)
print("\ntext seg for 0x22b450:", text_seg)
tv, to, tsz, tf = text_seg

md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

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

# ---- 全 text 段 BL xref ----
print("\n===== BL xref (full) =====")
code = data[to:to+tsz]
bl_hits = {}
for ins in md.disasm(code, tv):
    if ins.mnemonic == 'bl' and ins.operands:
        tgt = ins.operands[0].imm
        if tgt in targets:
            bl_hits.setdefault(targets[tgt], []).append(ins.address)
for name, addrs in sorted(bl_hits.items()):
    print(f"  {name:42s} <- {len(addrs)}x: {', '.join(hex(a) for a in addrs[:16])}")

# ---- curl 相关符号检查 ----
print("\n===== curl 符号检查 =====")
curl_syms = [b"curl_easy_setopt", b"curl_easy_init", b"curl_easy_perform",
             b"CURLOPT_SSL_VERIFYPEER", b"CURLOPT_SSL_VERIFYHOST",
             b"CURLOPT_PINNEDPUBLICKEY", b"curl_version", b"libcurl"]
for s in curl_syms:
    cnt = data.count(s)
    print(f"  {s.decode():28s}: {cnt}")

# curl 版本串
m = re.search(rb"libcurl/[0-9.]+", data)
mm = re.search(rb"curl/[0-9.]+", data)
if m: print("  curl version:", m.group(0).decode())
if mm: print("  curl small:", mm.group(0).decode())
# OpenSSL version string in this lib
m2 = re.search(rb"OpenSSL [0-9][0-9a-z.]*", data)
if m2: print("  openssl str:", m2.group(0).decode())