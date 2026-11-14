# -*- coding: utf-8 -*-
"""批量反编译 PLAINS 内 279 个唯一脚本: 主函数伪代码 + 子函数(方法名/常量)提取
输出: REV_ALL2/<src_path>.rev.lua  +  REV_ALL2/_API_REPORT.txt
"""
import json, os, sys, glob, struct, re

sys.path.insert(0, r"C:\Users\20751\Desktop\猫和老鼠")
from vm_rev_decompiler import parse_proto, Decompiler

ROOT = r"C:\Users\20751\Desktop\猫和老鼠\PLAINS"
OUT = r"C:\Users\20751\Desktop\猫和老鼠\REV_ALL2"
os.makedirs(OUT, exist_ok=True)

idx = json.load(open(os.path.join(ROOT, "_src_index.json"), encoding="utf-8"))

# 唯一脚本 -> 最佳缓冲(取最大的那个)
best = {}
for rel, size, status, src in idx:
    if status != "OK":
        continue
    s = src.lstrip("@").rstrip("\x00")
    if not s.startswith("src/"):
        continue
    full = os.path.join(ROOT, rel.replace("/", os.sep))
    if s not in best or size > best[s][1]:
        best[s] = (full, size)

def walk_protos(p, depth=0, out=None):
    """递归提取子函数常量(方法名线索)"""
    if out is None:
        out = []
    out.append((depth, p['code'], p['consts'], p['protos']))
    for sp in p['protos']:
        walk_protos(sp, depth + 1, out)
    return out

api_lines = []
stats = {"ok": 0, "fail": 0, "empty": 0}

for s in sorted(best.keys()):
    fpath, size = best[s]
    outname = s.replace("/", "_").replace("\\", "_")
    outp = os.path.join(OUT, outname + ".rev.lua")
    try:
        b = open(fpath, "rb").read()
        r = parse_proto(b)
        if r is None:
            stats["fail"] += 1
            continue
        ep, p = r
        lines = [f"-- [[ {s} ]]  src={s} size={size}"]
        lines.append(f"-- top: code={len(p['code'])} consts={len(p['consts'])} protos={len(p['protos'])}")
        lines.append("")
        d = Decompiler(p)
        body = d.run()
        lines.append(body)
        # 子函数方法名提取
        protos = walk_protos(p)
        methods = []
        for depth, code, consts, sps in protos[1:]:
            for c in consts:
                if isinstance(c, str) and re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]{1,63}", c):
                    methods.append(c)
        # 主函数常量里的类名/require 名
        main_consts = [c for c in p['consts'] if isinstance(c, str) and len(c) > 1]
        if methods:
            lines.append("")
            lines.append("-- SUBFUNCTIONS: " + ", ".join(sorted(set(methods))[:80]))
        api_lines.append(f"### {s}")
        api_lines.append(f"- top: code={len(p['code'])} consts={len(p['consts'])} protos={len(p['protos'])}")
        api_lines.append(f"- consts: {main_consts[:25]}")
        if methods:
            api_lines.append(f"- methods: {', '.join(sorted(set(methods))[:60])}")
        api_lines.append("")
        open(outp, "w", encoding="utf-8").write("\n".join(lines))
        stats["ok"] += 1
    except Exception as e:
        stats["fail"] += 1
        open(outp + ".err", "w", encoding="utf-8").write(repr(e))

open(os.path.join(OUT, "_API_REPORT.txt"), "w", encoding="utf-8").write("\n".join(api_lines))
print(stats, "output:", OUT)