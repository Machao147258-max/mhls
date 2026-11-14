# -*- coding: utf-8 -*-
# Proto 指针追踪验证: 找指向指定 TString 的 8字节指针(source 字段)
# 用法: python proto_probe.py <名字子串>
import sys, glob, struct

NAME = sys.argv[1].encode() if len(sys.argv) > 1 else b'MigrationRewardConfig.lua'

segs = []  # (base_va, data)
for f in sorted(glob.glob(r'C:\Users\20751\tomdump\dd_out\seg_*.bin')):
    base = int(f.rsplit('\\', 1)[-1].split('_')[1], 16)
    segs.append((base, open(f, 'rb').read()))

# 1. 找到所有包含该名字的 TString(名字前面通常有 @src/... 前缀)
targets = []
for base, d in segs:
    i = 0
    while True:
        j = d.find(NAME, i)
        if j < 0: break
        # 回溯找 @src/ 前缀起点(名字 TString 的完整内容)
        s = d.rfind(b'@src/', 0, j)
        start = s if s >= 0 and j - s < 120 else j
        va = base + start
        targets.append((va, base + j))
        i = j + 1
print('名字出现:', len(targets))
for va, _ in targets[:8]:
    print('  TString VA = %#x' % va)

# 2. 在所有段里搜指向这些 VA 的 8 字节指针(小端)
refs = []
for va, _ in targets:
    p = struct.pack('<Q', va)
    for base, d in segs:
        i = 0
        while True:
            j = d.find(p, i)
            if j < 0: break
            refs.append((va, base + j, base))
            i = j + 1
print('指向名字的指针:', len(refs))
for va, ref_va, base in refs[:15]:
    off = ref_va - base
    print(f'  名字 {va:#x} <- 指针位于 {ref_va:#x} (段内偏移 {off:#x})')