# -*- coding: utf-8 -*-
"""查证: 0x108230 符号身份 + X509_check_host/SSL_set1_host 存在性 + 全库 X509 校验函数清单"""
import os, subprocess, re, struct
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = r"C:\Users\20751\Desktop\猫和老鼠"
SO = os.path.join(ROOT, "lib_arm64", "tom_lib", "libAudioCommon.so")
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# 1) readelf -Ws 全符号找 0x108230 及 X509_check_host / ssl_verify 相关
r = subprocess.run(["readelf", "-Ws", SO], capture_output=True, timeout=120)
rtxt = (r.stdout or b'').decode('utf-8', 'replace')

print("=== 符号 0x108230 附近 ===")
for ln in rtxt.splitlines():
    if '0000000000108230' in ln or '1082300' in ln:
        print(" ", ln.strip())
    m = re.search(r'([0-9a-f]{16})\s+\d+\s+\S+\s+\S+\s+\S+\s+(\S+)\s*$', ln.strip()) if ln.strip() else None

print("\n=== X509_check_host / verify 相关符号 ===")
for ln in rtxt.splitlines():
    if re.search(r'\b(X509_check_host|SSL_set1_host|SSL_set_hostflags|X509_VERIFY_PARAM_set1_host|ssl_verify_cert_chain|X509_verify_cert(?!\S)|X509_verify)\b', ln):
        print(" ", ln.strip()[:170])

# 2) 反汇编 0x108230 (40 条)
print("\n=== 0x108230 反汇编 ===")
off = 0x108230  # vaddr == fileoff? 需段映射
# 简单: 假定 vaddr->off 用 PHDR
def load_segments(data):
    e_phoff = struct.unpack_from('<Q', data, 32)[0]
    e_phentsize = struct.unpack_from('<H', data, 54)[0]
    e_phnum = struct.unpack_from('<H', data, 56)[0]
    fmt = '<IIQQQQQQ'
    segs = []
    for i in range(e_phnum):
        o = e_phoff + i * e_phentsize
        p_type, p_fl, p_off, p_vaddr, p_paddr, p_fsz, p_msz, p_align = struct.unpack_from(fmt, data, o)
        if p_type == 1:
            segs.append((p_vaddr, p_off, p_fsz))
    return segs
segs = load_segments(data)
def v2o(v):
    for vv, oo, ss in segs:
        if vv <= v < vv + ss:
            return oo + (v - vv)
    return None

off2 = v2o(0x108230)
if off2:
    code = data[off2:off2+0x400]
    for ins in md.disasm(code, 0x108230):
        print(f"  0x{ins.address:x}: {ins.mnemonic:10s} {ins.op_str}")
        if ins.address > 0x1082f0:
            break
else:
    print("v2o fail")