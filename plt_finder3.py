# -*- coding: utf-8 -*-
"""v3: START=0x200000 扫 PLT stub + BL->stub 业务调用者 (SSL 使用点)"""
import os, struct, subprocess, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = r"C:\Users\20751\Desktop\猫和老鼠"
SO = os.path.join(ROOT, "lib_arm64", "tom_lib", "libAudioCommon.so")
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# readelf -r 窄格式
r = subprocess.run(["readelf", "-r", SO], capture_output=True, timeout=120)
rtxt = (r.stdout or b'').decode('utf-8', 'replace')
got_to_sym = {}
for ln in rtxt.splitlines():
    m = re.match(r'\s*([0-9a-f]{8,})\s+[0-9a-f]+\s+R_AARCH64_JUMP_SL\s+[0-9a-f]+\s+(\S+)', ln)
    if m:
        got_to_sym[int(m.group(1), 16)] = m.group(2)

want = {"SSL_CTX_new", "SSL_new", "SSL_read", "SSL_write", "SSL_connect",
        "SSL_do_handshake", "ssl_verify_cert_chain", "X509_verify_cert",
        "BIO_read", "BIO_write", "SSL_CTX_set_verify", "SSL_get_verify_result"}

START, END = 0x200000, 0x3b5000
code = data[START:END]
insns = list(md.disasm(code, START))
print("insns:", len(insns))

# PLT stub: adrp x16 / ldr x17,[x16,#..] / add x16,x16,#.. / br x17
plt_got = {}
for i in range(len(insns)-4):
    a0, a1, a2, a3 = insns[i], insns[i+1], insns[i+2], insns[i+3]
    if (a0.mnemonic == 'adrp' and a0.op_str.startswith('x16') and
        a1.mnemonic == 'ldr' and a1.op_str.startswith('x17') and
        a2.mnemonic == 'add' and a2.op_str.startswith('x16, x16') and
        a3.mnemonic == 'br' and a3.op_str == 'x17'):
        mimm = re.search(r'#(0x[0-9a-f]+)', a1.op_str)
        if mimm:
            got = a0.operands[0].imm + int(mimm.group(1), 16)
            plt_got[a0.address] = got
print("PLT stubs:", len(plt_got))

stub_addr = set(plt_got.keys())
callers = {}
for ins in insns:
    if ins.mnemonic == 'bl' and ins.operands:
        tgt = ins.operands[0].imm
        if tgt in stub_addr:
            got = plt_got[tgt]
            sym = got_to_sym.get(got, hex(got))
            callers.setdefault(sym, []).append(ins.address)

print("\n=== BL -> PLT stub 业务调用者 ===")
for sym, addrs in sorted(callers.items()):
    if any(w in sym for w in ["SSL_", "ssl_", "X509", "BIO_"]):
        print(f"  {sym:40s} <- {len(addrs)}x: {', '.join(hex(a) for a in addrs[:20])}")

# 针对核心目标的调用者上下文
print("\n=== 核心函数调用者上下文 ===")
core = ["SSL_CTX_new", "SSL_new", "SSL_read", "SSL_write", "ssl_verify_cert_chain", "X509_verify_cert"]
for sym, addrs in callers.items():
    if sym in core and addrs:
        for a in addrs[:4]:
            st, en = a - 12, a + 16
            ctx = data[st:en]
            lines = []
            for ins in md.disasm(ctx, st):
                marker = "  <<<< call" if ins.address == a else ""
                lines.append(f"      0x{ins.address:x}: {ins.mnemonic:8s} {ins.op_str}{marker}")
            print(f"  {sym} @ 0x{a:x}:")
            print("\n".join(lines))