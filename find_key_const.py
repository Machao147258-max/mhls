# -*- coding: utf-8 -*-
# 决定性搜索: 内存 dump 中 luac 常量池的 16 字节 key 字符串
# 格式: \x04 <len:u32> <data...> (len 含 NUL)
# len=17 → 16 字符 key; len=16 → 15 字符; 也搜 13-20 范围
import os, struct

DIRS = [r'C:\Users\20751\tomdump\dd_live_1973', r'C:\Users\20751\tomdump\dd_live_6894',
        r'C:\Users\20751\tomdump\dd_out', r'C:\Users\20751\tomdump\mem_live',
        r'C:\Users\20751\tomdump\mem_live2', r'C:\Users\20751\tomdump\mem_scan',
        r'C:\Users\20751\tomdump\mem_hits', r'C:\Users\20751\tomdump\mem_scudo']
hits = []
files = []
for d in DIRS:
    if not os.path.isdir(d): continue
    for f in os.listdir(d):
        p = os.path.join(d, f)
        try:
            if os.path.getsize(p) < 4096: continue
        except: continue
        files.append(p)
files.append(r'C:\Users\20751\tomdump\mega\all.bin')
print(f'扫描 {len(files)} 文件', flush=True)

for p in files:
    try:
        b = open(p, 'rb').read()
    except: continue
    i = 0
    while True:
        i = b.find(b'\x04', i)
        if i < 0: break
        if i + 5 <= len(b):
            ln = struct.unpack_from('<I', b, i+1)[0]
            if 13 <= ln <= 22 and i + 5 + ln <= len(b):
                s = b[i+5:i+5+ln-1]
                # 排除明显的非 key (含 / @ 或过长可打印)
                try:
                    s.decode('ascii')
                except:
                    i += 1
                    continue
                if any(c in s for c in b'/@\\\x00') and ln < 20:
                    i += 1
                    continue
                hits.append((p, i, ln, s))
                if len(hits) > 200:
                    print('太多命中, 停止', flush=True)
                    i = len(b)
                    break
        i += 1

print(f'命中 {len(hits)}', flush=True)
for p, i, ln, s in hits[:120]:
    print(f'{os.path.basename(p)} @{hex(i)} len={ln} {s!r}', flush=True)
