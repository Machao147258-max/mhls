# -*- coding: utf-8 -*-
"""完整 PLT 表映射: 扫 0x100000-0x200000 的 PLT stub -> GOT -> 符号; 再全业务代码找 BL->stub"""
import os, struct, subprocess, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = r"C:\Users\20751\Desktop\猫和老鼠"
SO = os.path.join(ROOT, "lib_arm64", "tom_lib", "libAudioCommon.so")
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# readelf -r 解析 GOT -> 符号
r = subprocess.run(["readelf", "-r", SO], capture_output=True, timeout=120)
rtxt = (r.stdout or b'').decode('utf-8', 'replace')
got_to_sym = {}
for ln in rtxt.splitlines():
    m = re.match(r'\s*([0-9a-f]{8,})\s+[0-9a-f]+\s+R_AARCH64_JUMP_SL\s+[0-9a-f]+\s+(\S+)', ln)
    if m:
        got_to_sym[int(m.group(1), 16)] = m.group(2)

# 扫 PLT 区 0x100000-0x1fffff
PLT_START, PLT_END = 0x100000, 0x200000
code = data[PLT_START:PLT_END]
stub_got = {}   # stub_addr -> got
stub_sym = {}   # stub_addr -> symname
for i in range(len(code)//4):
    a = PLT_START + i*4
    if i+3 < len(code)//4:
        b0 = data[a:a+4]
        # adrp x16, #page ; ldr x17, [x16, #off]; add x16, x16, #off; br x17
        insts = list(md.disasm(data[a:a+16], a))
        if len(insts) == 4:
            i0, i1, i2, i3 = insts
            if (i0.mnemonic=='adrp' and i0.op_str.startswith('x16') and
                i1.mnemonic=='ldr' and i1.op_str.startswith('x17') and
                i2.mnemonic=='add' and i2.op_str.startswith('x16, x16') and
                i3.mnemonic=='br' and i3.op_str=='x17'):
                mimm = re.search(r'#(0x[0-9a-f]+)', i1.op_str)
                if mimm:
                    got = i0.operands[0].imm + int(mimm.group(1),16)
                    stub_got[a] = got
                    stub_sym[a] = got_to_sym.get(got, hex(got))

print("PLT stubs:", len(stub_got))

# 反汇编业务代码找 BL -> stub
BIZ_START, BIZ_END = 0x200000, 0x3b5000
biz = data[BIZ_START:BIZ_END]
callers = {}
for ins in md.disasm(biz, BIZ_START):
    if ins.mnemonic=='bl' and ins.operands:
        tgt = ins.operands[0].imm
        if tgt in stub_sym:
            sym = stub_sym[tgt]
            callers.setdefault(sym, []).append(ins.address)

interesting = ["SSL_CTX_new","SSL_new","SSL_read","SSL_write","SSL_connect",
               "SSL_do_handshake","ssl_verify_cert_chain","X509_verify_cert",
               "BIO_read","BIO_write","SSL_CTX_set_verify","SSL_get_verify_result",
               "SSL_set_fd","SSL_set1_host","SSL_set_tlsext_host_name","X509_check_host"]
print("\n=== SSL 相关: BL->PLT 业务调用者 ===")
for sym, addrs in sorted(callers.items()):
    s = sym.split('@')[0]
    if any(w in s for w in ["SSL_","ssl_","X509","BIO_","tls_"]):
        print(f"  {s:42s} <- {len(addrs)}x: {', '.join(hex(a) for a in addrs[:24])}")