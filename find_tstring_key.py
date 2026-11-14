# -*- coding: utf-8 -*-
# 按 Lua TString 结构搜 key: len=16 (8B) 前有 hash/reserved, 后有 16B 数据
# TString(5.1, 64位): next(8) tt(1) marked(1) pad(6) reserved(1) pad(3) hash(4) len(8) data...
# 简化搜索: 任意 8B 前 + \x10*8 (len=16) + 16B 可打印
import re, struct, os, glob

files = glob.glob(r'C:\Users\20751\tomdump\live_heap\heap*.bin') + glob.glob(r'C:\Users\20751\tomdump\live_segs\*.bin')
cands = {}
print(f'扫描 {len(files)} 文件 (TString len=16/17 模式)', flush=True)
for fn in files:
    b = open(fn, 'rb').read()
    for ln in (16, 17):
        pat = struct.pack('<Q', ln)
        i = 0
        while True:
            i = b.find(pat, i)
            if i < 0: break
            data = b[i+8:i+8+16]
            try:
                data.decode('ascii')
            except:
                i += 1
                continue
            # 前面 12B 应有 reserved(0)+hash 特征 (hash 任意, reserved=0 常见)
            pre = b[max(0, i-12):i]
            # 过滤: data 全是可打印
            if all(32 <= c < 127 for c in data):
                cands[data] = cands.get(data, 0) + 1
            i += 1
print(f'TString 候选 {len(cands)}', flush=True)
# 保存候选列表
with open(r'C:\Users\20751\tomdump\tstring_cands.txt', 'w') as f:
    for c in sorted(cands):
        f.write(c.decode() + '\n')
# 打印出现次数 >1 的 (活跃字符串更可能是 key)
multi = [(c, n) for c, n in cands.items() if n > 1]
print(f'出现多次的: {len(multi)}', flush=True)
for c, n in sorted(multi, key=lambda x: -x[1])[:60]:
    print(f'  {n}x {c!r}', flush=True)
