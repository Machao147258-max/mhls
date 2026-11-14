# -*- coding: utf-8 -*-
"""check_heartbleed_static.py v4 — Heartbleed (CVE-2014-0160) 静态判定
v4 修正: 判定窗口 = [REQUEST 入口, vuln malloc)。1.0.1g 修复版在此窗口加入
        "if (1+2+payload+16 > s->s3->rrec.length) return 0" 比较; 1.0.1c 无。
        窗口外(RESPONSE 分支/msg_callback)一律不计。
输出: VULNERABLE / PATCHED / NOT_FOUND
用法: python check_heartbleed_static.py [so路径]
"""
import sys
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
if len(sys.argv) > 1:
    F = sys.argv[1]

HB_FN = 0xc858cc
MALLOC = 0xb99964

d = open(F, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM); md.skipdata = True
seq = list(md.disasm(d[HB_FN:HB_FN + 0x400], HB_FN))
if not seq or seq[0].mnemonic != 'stp':
    print("NOT_FOUND: no function at 0x%x" % HB_FN); sys.exit(0)

# 1) n2s 完成点
n2s_at = None
for i, ins in enumerate(seq):
    if ins.mnemonic == 'orr' and 'lsl #8' in ins.op_str and \
       any(seq[j].mnemonic == 'ldrb' for j in range(max(0, i-6), i)):
        n2s_at = ins.address; break

# 2) REQUEST 入口: b.eq 目标 (hbtype==1 分支)
req_entry = None
for i, ins in enumerate(seq):
    if ins.mnemonic == 'cmp' and ins.op_str.startswith('w22') and '#1' in ins.op_str:
        for j in range(i, min(i+4, len(seq))):
            if seq[j].mnemonic == 'b.eq':
                req_entry = int(seq[j].op_str[1:], 16); break
        break

# 3) vuln malloc: REQUEST 入口后 add #0x13 之后的 bl MALLOC
malloc_at = None
for i, ins in enumerate(seq):
    if ins.mnemonic == 'add' and '#0x13' in ins.op_str and (req_entry is None or ins.address >= req_entry):
        for j in range(i+1, min(i+8, len(seq))):
            if seq[j].mnemonic == 'bl' and int(seq[j].op_str[1:], 16) == MALLOC:
                malloc_at = seq[j].address; break
    if malloc_at: break

print("== Heartbleed static check v4 ==")
print("tls1_process_heartbeat @ 0x%x" % HB_FN)
print("n2s(payload) done      @ 0x%x" % (n2s_at or 0))
print("REQUEST entry          @ 0x%x" % (req_entry or 0))
print("vuln malloc (after +19)@ 0x%x" % (malloc_at or 0))
if not (n2s_at and req_entry and malloc_at):
    print("NOT_FOUND: heartbeat shape not matched"); sys.exit(0)

# 4) 判定窗口 [req_entry, malloc_at)
print("\n-- window [REQUEST entry -> malloc]: --")
vuln = True
for s in seq:
    if req_entry <= s.address < malloc_at:
        print("  0x%x: %-7s %s" % (s.address, s.mnemonic, s.op_str))
        if s.mnemonic in ('cmp', 'subs', 'adds') or s.mnemonic in ('b.hi', 'b.ls', 'b.ge', 'b.le', 'b.gt', 'b.lt', 'b.pl', 'b.mi'):
            vuln = False

print("\n== RESULT: %s ==" % (
    "VULNERABLE (CVE-2014-0160)\n"
    "  REQUEST path: n2s(payload) -> malloc(1+2+payload+16) -> memcpy(bp,pl,payload) -> echo(payload+19)\n"
    "  NO length check (1.0.1g fix `1+2+payload+16 > rrec.length -> discard` is MISSING).\n"
    "  payload_length=0xFFFF => OOB read + echo 64KB heap (session keys / payment tokens)."
    if vuln else "PATCHED (length check present before malloc)"))