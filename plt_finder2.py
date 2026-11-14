# -*- coding: utf-8 -*-
"""v2: 用 readelf -r (窄格式) 解析 GOT; capstone 找 PLT stub; 找 BL->stub 调用者
   同时检查根目录 unisec.so/secsdk.so (x86_64) 的 TLS 实现特征"""
import os, struct, subprocess, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = r"C:\Users\20751\Desktop\猫和老鼠"
SO = os.path.join(ROOT, "lib_arm64", "tom_lib", "libAudioCommon.so")
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# 1) readelf -r 窄格式解析
r = subprocess.run(["readelf", "-r", SO], capture_output=True, timeout=120)
rtxt = (r.stdout or b'').decode('utf-8', 'replace')
got_to_sym = {}
for ln in rtxt.splitlines():
    m = re.match(r'\s*([0-9a-f]{8,})\s+[0-9a-f]+\s+R_AARCH64_JUMP_SL\s+[0-9a-f]+\s+(\S+)', ln)
    if m:
        got_to_sym[int(m.group(1), 16)] = m.group(2)
print("JUMP_SL entries:", len(got_to_sym))
for g, s in sorted(got_to_sym.items()):
    print(f"  GOT 0x{g:x} -> {s}")

want = {"SSL_CTX_new", "SSL_new", "SSL_read", "SSL_write", "SSL_connect",
        "SSL_do_handshake", "ssl_verify_cert_chain", "X509_verify_cert",
        "BIO_read", "BIO_write", "SSL_CTX_set_verify"}

# 2) 全 text 反汇编: 找所有 GOT load (adrp x16,page / ldr x17,[x16,#off]), 记录 PLT stub = 紧跟 br x17 的
START, END = 0x0, 0x3b5000
code = data[START:END]
insns = list(md.disasm(code, START))
print("\ninsns:", len(insns))

# 识别 PLT stub 模式: [adrp x16,page] [ldr x17,[x16,#off]] [add x16,x16,#off] [br x17]
plt_got = {}  # stub_addr -> got addr
for i in range(len(insns)-4):
    a0, a1, a2, a3 = insns[i], insns[i+1], insns[i+2], insns[i+3]
    if (a0.mnemonic == 'adrp' and a0.op_str.startswith('x16') and
        a1.mnemonic == 'ldr' and a1.op_str.startswith('x17') and
        a2.mnemonic == 'add' and a2.op_str.startswith('x16, x16') and
        a3.mnemonic == 'br' and a3.op_str == 'x17'):
        # 解析 GOT 地址: ldr x17,[x16,#imm] -> page(a0.imm) + imm
        mimm = re.search(r'#(0x[0-9a-f]+)', a1.op_str)
        if mimm:
            got = a0.operands[0].imm + int(mimm.group(1), 16)
            plt_got[a0.address] = got
print("PLT stubs found:", len(plt_got))

# 3) 找 BL 到 PLT stub 的调用者 (业务调用点)
stub_addr = set(plt_got.keys())
callers = {}  # symname -> [caller addr]
for ins in insns:
    if ins.mnemonic == 'bl' and ins.operands:
        tgt = ins.operands[0].imm
        if tgt in stub_addr:
            got = plt_got[tgt]
            sym = got_to_sym.get(got, hex(got))
            callers.setdefault(sym, []).append(ins.address)

print("\n=== BL -> PLT stub (业务调用 SSL 函数) ===")
for sym, addrs in sorted(callers.items()):
    if sym in want or True:
        print(f"  {sym:34s} <- {len(addrs)}x: {', '.join(hex(a) for a in addrs[:30])}")

# 4) 根目录 unisec.so / secsdk.so TLS 特征
print("\n=== 根目录易盾库 TLS 特征 ===")
for fn in ["unisec.so", "secsdk.so"]:
    p = os.path.join(ROOT, fn)
    try:
        d = open(p, 'rb').read()
    except Exception as e:
        print(fn, "ERR", e); continue
    e_machine = struct.unpack_from('<H', d, 18)[0] if d[:4] == b'\x7fELF' else '?'
    print(f"{fn:14s} size={len(d):>9d} machine={e_machine}")
    probes = {
        "OpenSSL": d.count(b"OpenSSL"),
        "BoringSSL": d.count(b"BoringSSL"),
        "libssl string": d.count(b"libssl"),
        "SSL_CTX_new": d.count(b"SSL_CTX_new"),
        "SSL_read": d.count(b"SSL_read"),
        "X509_verify_cert": d.count(b"X509_verify_cert"),
        "BEGIN CERT": d.count(b"-----BEGIN CERT"),
        "gRPC": d.count(b"grpc"),
        "TLS1.3": d.count(b"TLS 1.3") + d.count(b"TLS1.3"),
        "GmSSL": d.count(b"GmSSL"),
        "mbedTLS": d.count(b"mbedtls") + d.count(b"mbedTLS"),
    }
    hit = {k: v for k, v in probes.items() if v}
    print("   ", hit if hit else "  (无 TLS 实现特征)")