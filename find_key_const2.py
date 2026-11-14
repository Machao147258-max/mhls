# -*- coding: utf-8 -*-
# 严格过滤器: luac 常量池 type-4 字符串 (len 含 NUL, 13-20B)
# 要求: 前面 8 字节内无 \x00 连续垃圾; 串后可打印或为下一个类型字节
import os, struct

DIRS = [r'C:\Users\20751\tomdump\dd_live_1973', r'C:\Users\20751\tomdump\dd_live_6894',
        r'C:\Users\20751\tomdump\dd_out', r'C:\Users\20751\tomdump\mem_live',
        r'C:\Users\20751\tomdump\mem_live2', r'C:\Users\20751\tomdump\mem_scan',
        r'C:\Users\20751\tomdump\mem_hits', r'C:\Users\20751\tomdump\mem_scudo']
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

results = []
for p in files:
    try:
        b = open(p, 'rb').read()
    except: continue
    for ln in (17, 16, 15, 18, 14, 19, 13, 20):  # len 含 NUL
        pat = b'\x04' + struct.pack('<I', ln)
        i = 0
        while True:
            i = b.find(pat, i)
            if i < 0: break
            s = b[i+5:i+5+ln-1]
            # 1) 全部可打印
            try:
                s.decode('ascii')
            except:
                i += 1
                continue
            # 2) 串后字节: 必须是 \x00 (NUL) 或 常量类型字节 0/1/3/4 或 下一个串长度低字节
            nxt = b[i+5+ln] if i+5+ln < len(b) else 0
            if nxt not in (0, 1, 3, 4, 5, 6, 8, 9, 10, 12, 14, 16, 32):
                i += 1
                continue
            # 3) 前面 6 字节不全是 \x00 (排除二进制误报)
            pre = b[max(0, i-6):i]
            if pre.count(0) > 4:
                i += 1
                continue
            results.append((os.path.basename(p), i, ln, s))
            i += 1

print(f'严格命中 {len(results)}', flush=True)
seen = set()
for f, i, ln, s in results:
    if s in seen: continue
    seen.add(s)
    print(f'{f} @{hex(i)} len={ln} {s!r}', flush=True)
