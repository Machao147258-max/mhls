# -*- coding: utf-8 -*-
"""找 PLT stub 地址 -> 找 BL 到 PLT stub 的业务调用者 (SSL 真正使用方)
   另: 全局搜索 unisec.so / secsdk.so 位置"""
import os, struct, subprocess, re
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT = r"C:\Users\20751\Desktop\猫和老鼠"
SO = os.path.join(ROOT, "lib_arm64", "tom_lib", "libAudioCommon.so")
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

# 1) PLT: readelf -r 给 GOT 地址; readelf -S 找 .plt 段 (若 section 头剥离则用 PHDR)
r = subprocess.run(["readelf", "-rW", SO], capture_output=True, timeout=120)
rtxt = (r.stdout or b'').decode('utf-8', 'replace')

got_to_sym = {}
for ln in rtxt.splitlines():
    m = re.match(r'\s*([0-9a-f]+)\s+[0-9a-f]+\s+R_AARCH64_JUMP_SL\s+[0-9a-f]+\s+(\S+)', ln)
    if m:
        got_to_sym[int(m.group(1), 16)] = m.group(2)
print("JUMP_SL entries:", len(got_to_sym))
for g, s in sorted(got_to_sym.items()):
    print(f"  GOT 0x{g:x} -> {s}")

# 2) 找 PLT stub: 在 text 段扫描 "adrp x16, GOTpage; ldr x17,[x16,#off]; add x16...; br x17" 模板
#    PLT stub 通常紧邻 .plt 区, 查找 BLR/BR 到 GOT 内容
# 简单方案: 找所有 "ldr xN,[pc+imm]" 中 PC-relative 目标 = GOT 地址 的指令 (GOT load), 即取函数指针
want_got = {0x3dd938: "SSL_CTX_new", 0x3ddc78: "SSL_read", 0x3df8c8: "SSL_write",
            0x3df7d0: "SSL_new", 0x3dad80: "SSL_connect", 0x3df6a0: "SSL_do_handshake",
            0x3dc918: "ssl_verify_cert_chain", 0x3ddb60: "X509_verify_cert",
            0x3df3a8: "BIO_write", 0x3e0990: "BIO_read"}

# 反汇编 0x0 - 0x3b5000 (text) 找 ldr/ldur 取 GOT, 然后看下一个 insn 是否 blr
START, END = 0x0, 0x3b5000
code = data[START:END]
loads = []  # (addr, got_addr, symname, reg)
insns = list(md.disasm(code, START))
for i, ins in enumerate(insns):
    if ins.mnemonic in ('ldr', 'ldur'):
        # PC-relative: ldr xN, [pc, #imm] -> target = ((addr+4)&~3) + imm
        for op in ins.operands:
            if op.type == 4 and op.mem.base == 1 and op.mem.index == -1:  # mem PC-relative (base=pc? capstone pc=arch)
                pass
        # capstone: ldr x8, [pc, #imm] => op_str 形如 "[pc, #0x...]" 或标号
        if 'pc' in ins.op_str or '#' in ins.op_str:
            m2 = re.match(r'x(\d+), \[pc, #(0x[0-9a-f]+)\]', ins.op_str)
            if m2:
                reg = m2.group(1)
                imm = int(m2.group(2), 16)
                tgt = ((ins.address + 4) & ~3) + imm
                if tgt in want_got:
                    loads.append((ins.address, tgt, want_got[tgt], reg))

print("\n=== GOT loads (取 SSL 函数指针处) ===")
# 对每个 load, 看紧邻指令是否 blr rN / br rN
load_set = set(a for a, _, _, _ in loads)
for a, g, s, reg in loads:
    # 找后续 1-4 条指令中的 blr x{reg}
    use = "?"
    for j in range(1, 6):
        idx = insns.index((lambda ii: ii)(next(x for x in insns if x.address == a)))
        break
    print(f"  0x{a:x}: ldr x{reg} <- GOT[{s}]")

# 用 insns 列表做前向搜索
idxmap = {ins.address: i for i, ins in enumerate(insns)}
for a, g, s, reg in loads:
    i = idxmap.get(a)
    if i is None:
        continue
    follow = []
    for k in range(i+1, min(i+6, len(insns))):
        nxt = insns[k]
        follow.append(f"{nxt.mnemonic} {nxt.op_str}")
        if nxt.mnemonic in ('blr', 'br'):
            break
    print(f"  0x{a:x}: [{s}] -> 后续: {'; '.join(follow)}")
    # 记调用者(找函数起始: 向上找最近 stp x29/x30 或 bti/sub sp)
    if follow and ('blr' in follow[-1] or 'br' in follow[-1]):
        # 向上定位函数头: 从 a 向上找指令含 'stp.*x29.*x30' 或 'sub.*sp.*#' 
        fn_start = None
        for k in range(i, max(0, i-400), -1):
            p = insns[k]
            if p.mnemonic == 'stp' and 'x29' in p.op_str and 'x30' in p.op_str:
                fn_start = p.address
                break
            if p.mnemonic == 'sub' and 'sp' in p.op_str and (k == 0 or insns[k-1].address != p.address - 4):
                pass
        print(f"      ^ 疑似函数: 0x{fn_start:x}" if fn_start else "      ^ 函数头未定位")

# 3) unisec.so / secsdk.so 位置
print("\n=== 搜索 unisec.so / secsdk.so ===")
for root, dirs, files in os.walk(ROOT):
    for f in files:
        if f in ("unisec.so", "secsdk.so", "libunisec.so", "libsec-lib.so"):
            print(" ", os.path.join(root, f))