# -*- coding: utf-8 -*-
"""扫描 GOT 间接调用 (ADRP xN,gpage; LDR xM,[xN,#off]; ...; BLR xM) 定位 SSL 业务调用点
   同时检查 0x0-0x100000 是否含代码"""
import os, subprocess, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = r"C:\Users\20751\Desktop\猫和老鼠"
SO = os.path.join(ROOT, "lib_arm64", "tom_lib", "libAudioCommon.so")
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# GOT -> 符号
r = subprocess.run(["readelf", "-r", SO], capture_output=True, timeout=120)
rtxt = (r.stdout or b'').decode('utf-8', 'replace')
got_to_sym = {}
for ln in rtxt.splitlines():
    m = re.match(r'\s*([0-9a-f]{8,})\s+[0-9a-f]+\s+R_AARCH64_JUMP_SL\s+[0-9a-f]+\s+(\S+)', ln)
    if m:
        got_to_sym[int(m.group(1), 16)] = m.group(2)

# 目标 GOT 条目 (之前 got_unisdk_scan 确认)
want_got = {
    0x3dd938: "SSL_CTX_new", 0x3df7d0: "SSL_new", 0x3ddc78: "SSL_read",
    0x3df8c8: "SSL_write", 0x3dad80: "SSL_connect", 0x3df6a0: "SSL_do_handshake",
    0x3dc918: "ssl_verify_cert_chain", 0x3ddb60: "X509_verify_cert",
    0x3df3a8: "BIO_write", 0x3e0990: "BIO_read", 0x3e19a8: "SSL_get_peer_certificate",
    0x3e1950: "SSL_CTX_set_verify*", 0x3e1930: "SSL_set1_host*",
}
# 从 got_to_sym 精确找
exact = {}
for g, s in got_to_sym.items():
    base = s.split('@')[0]
    if base in ("SSL_CTX_new","SSL_new","SSL_read","SSL_write","SSL_connect",
                "SSL_do_handshake","ssl_verify_cert_chain","X509_verify_cert",
                "BIO_read","BIO_write","SSL_CTX_set_verify","SSL_set1_host",
                "SSL_get_verify_result","SSL_set_fd","SSL_ctrl","SSL_set_tlsext_host_name"):
        exact[g] = base

print("目标 GOT 符号:")
for g, s in sorted(exact.items()):
    print(f"  GOT 0x{g:x} -> {s}")

# 找 GOT 间接调用: 扫描 0x200000-0x3b5000, 找 ldr xM,[xN,#imm] 或 ldr xM,[xN] 后跟 blr xM
# 策略: 先收集所有 ldr 指令, 解析出加载的 GOT 地址, 再看后续 blr/br
BIZ_START, BIZ_END = 0x200000, 0x3b5000
biz = data[BIZ_START:BIZ_END]
insns = list(md.disasm(biz, BIZ_START))
print(f"\n业务代码指令: {len(insns)}")

# 记录 ldr reg, [reg2, #imm] 且 reg2 源自 adrp 的 GOT 解析
# 简化: 逐条扫描, 遇到 ldr xM,[xN,#imm], 反向找最近的 adrp xN 计算 got 地址
adrp_map = {}  # addr -> (reg, page)
got_loads = []  # (instr_addr, reg, gotaddr)
for i, ins in enumerate(insns):
    if ins.mnemonic == 'adrp':
        m = re.match(r'x(\d+), #(0x[0-9a-f]+)', ins.op_str)
        if m:
            adrp_map[ins.address] = (int(m.group(1)), int(m.group(2), 16))
    elif ins.mnemonic in ('ldr','ldur') and '#' in ins.op_str:
        m = re.match(r'x(\d+), \[x(\d+), #(0x[0-9a-f]+)\]', ins.op_str)
        if m:
            rM, rN, imm = int(m.group(1)), int(m.group(2)), int(m.group(3), 16)
            # 找最近(前 20 条内) adrp 设置 xN
            for j in range(i-1, max(0, i-60), -1):
                if insns[j].address in adrp_map:
                    rN2, page = adrp_map[insns[j].address]
                    if rN2 == rN:
                        got = page + imm
                        if got in exact and 0x3d0000 <= got < 0x3e3000:
                            got_loads.append((ins.address, rM, got, exact[got]))
                        break

print("\nGOT 间接加载 (ADRP+LDR -> GOT):")
for a, rm, got, sym in got_loads:
    print(f"  0x{a:x}: ldr x{rm} <- GOT[0x{got:x}] = {sym}")
    # 找后续 blr x{rm}
    for j in range(len(insns)):
        if insns[j].address == a:
            for k in range(j+1, min(j+8, len(insns))):
                nxt = insns[k]
                if nxt.mnemonic == 'blr' and nxt.op_str == f'x{rm}':
                    print(f"       -> BLR x{rm} @ 0x{nxt.address:x}")
                if nxt.mnemonic in ('blr','b','bl','br','ret'):
                    break
            break