# -*- coding: utf-8 -*-
"""修正2: 从 0x218000 起反汇编 (跳过 ELF 头), 全量 BL xref"""
import struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so"
data = open(SO, 'rb').read()

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
# 反汇编边界: 覆盖 0x200000 ~ 0x2b8000 的 .text
START, END = 0x200000, 0x2c0000
code = data[START:END]
bl_hits = {}
cnt = 0
for ins in md.disasm(code, START):
    cnt += 1
    if ins.mnemonic == 'bl' and ins.operands:
        tgt = ins.operands[0].imm
        if tgt in targets:
            bl_hits.setdefault(targets[tgt], []).append(ins.address)
print(f"disasm instrs: {cnt}")
for name, addrs in sorted(bl_hits.items()):
    print(f"  {name:42s} <- {len(addrs)}x: {', '.join(hex(a) for a in addrs[:20])}")

# 额外: 也看 target 附近的调用上下文 - 把调用者反汇编前后几行给出来
print("\n===== caller context (top 3 per target) =====")
for name, addrs in sorted(bl_hits.items()):
    shown = 0
    for a in addrs[:6]:
        st, en = a - 16, a + 20
        ct = data[st:en]
        lines = []
        for ins in md.disasm(ct, st):
            marker = " <<<<" if ins.address == a else ""
            lines.append(f"       0x{ins.address:x}: {ins.mnemonic:8s} {ins.op_str}{marker}")
        print(f"  {name} caller @ 0x{a:x}:")
        print("\n".join(lines))
        shown += 1
        if shown >= 3:
            break