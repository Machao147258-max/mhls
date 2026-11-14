# -*- coding: utf-8 -*-
"""扩大全段扫描 (0x200000-0x3b5000), 找 ssl_verify_cert_chain / SSL_CTX_new / set_verify 调用者"""
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so"
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

targets = {
    0x212894: "ssl_verify_cert_chain",
    0x21b7a8: "SSL_CTX_new",
    0x21bba8: "SSL_CTX_set_verify",
    0x21bba0: "SSL_CTX_set_cert_verify_callback",
    0x2a2dd4: "X509_verify_cert",
    0x22b450: "tls_process_server_certificate",
    0x21ca68: "SSL_get_verify_result",
    0x217634: "SSL_new",
    0x219df4: "SSL_read",
    0x21a2d0: "SSL_write",
    0x21c9a0: "SSL_CTX_set_default_verify_paths",
    0x21ca58: "SSL_CTX_load_verify_locations",
    0x2a09e4: "X509_STORE_add_cert",
    0x219ab0: "SSL_connect",
    0x2199c4: "SSL_do_handshake",
    0x21dbfc: "ssl_log_secret",
}
START, END = 0x200000, 0x3b5000
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
    print(f"  {name:40s} <- {len(addrs)}x: {', '.join(hex(a) for a in addrs[:25])}")