# -*- coding: utf-8 -*-
# 探测各匿名段: 抓每段前 64KB, 搜 X1V5fzTo / luac 头 / 默认key, 命中列表输出
import subprocess, sys, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
pid = sys.argv[1]

def sh(a, t=120):
    r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + a, capture_output=True, timeout=t)
    return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()

out = sh(['shell', f'su -c "cat /proc/{pid}/maps"'])
segs = []
for l in out.splitlines():
    p = l.split()
    if len(p) < 2: continue
    try:
        s, e = p[0].split('-')
        s, e = int(s, 16), int(e, 16)
    except: continue
    if 'rw' not in p[1]: continue
    if s < 0x400000000000 and not (0x2000000 <= s < 0xe000000): continue  # 只探测用户区
    if e - s < 0x10000: continue
    segs.append((s, e, p[1]))

print(f'候选段 {len(segs)}', flush=True)
hits = []
for s, e, perm in segs:
    page = s >> 12
    r = sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count=16 2>/dev/null | head -c 65536 | base64 -w0"'], t=60)
    if not r or r == 'ERR':
        continue
    import base64
    try:
        chunk = base64.b64decode(r)
    except Exception:
        continue
    marks = []
    if b'X1V5fzTo' in chunk: marks.append('X1V5fzTo')
    if b'\x1bLuaQ' in chunk: marks.append('LUAC')
    if bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b') in chunk: marks.append('KEY1')
    if marks:
        hits.append((s, e, marks))
        print(f'★ {hex(s)}-{hex(e)} ({perm}) {marks} size={hex(e-s)}', flush=True)

print(f'\n命中 {len(hits)} 段', flush=True)
with open(rf'C:\Users\20751\tomdump\seg_hits_{pid}.txt', 'w') as f:
    for s, e, marks in hits:
        f.write(f'{hex(s)} {hex(e)} {marks}\n')
print('已保存 seg_hits', flush=True)
