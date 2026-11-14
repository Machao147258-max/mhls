# -*- coding: utf-8 -*-
# 全量抓取命中段 + 本地分析
import subprocess, os, base64, re, struct

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
pid = '18380'
SEGS = [
    ('0x778eba697000', '0x778eba7d7000', 'x1_enc'),
    ('0x77904a6d5000', '0x77904a815000', 'x2_luac'),
    ('0x77909a69d000', '0x77909a71d000', 'x3_enc'),
    ('0x779155632000', '0x779155646000', 'x4_luac'),
    ('0x7791557f3000', '0x77915580a000', 'x5_luac'),
    ('0x7791587ba000', '0x7791587cc000', 'x6_luac'),
    ('0x77915beaf000', '0x77915bed4000', 'x7_luac'),
    ('0x779167e94000', '0x779167eab000', 'x8_luac'),
    ('0x779168c23000', '0x779168c3b000', 'x9_luac'),
    ('0x77916c248000', '0x77916c25b000', 'x10_enc'),
    ('0x779170c22000', '0x779170c52000', 'x11_luac'),
    ('0x77917799e000', '0x7791779b5000', 'x12_luac'),
]

def sh(a, t=180):
    r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + a, capture_output=True, timeout=t)
    return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()

os.makedirs(r'C:\Users\20751\tomdump\live_segs', exist_ok=True)
for s, e, name in SEGS:
    start, end = int(s, 16), int(e, 16)
    page, n = start >> 12, (end - start + 4095) >> 12
    dev = f'/data/local/tmp/seg_{name}.bin'
    sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={n} of={dev} 2>&1"'])
    r = sh(['pull', dev, rf'C:\Users\20751\tomdump\live_segs\{name}.bin'])
    print(f'{name}: {hex(end-start)}B pulled', flush=True)

# 本地分析
print('\n=== 分析 ===', flush=True)
for fn in sorted(os.listdir(r'C:\Users\20751\tomdump\live_segs')):
    b = open(rf'C:\Users\20751\tomdump\live_segs\{fn}', 'rb').read()
    n_x = b.count(b'X1V5fzTo')
    n_l = b.count(b'\x1bLuaQ')
    print(f'{fn}: {len(b)}B X1V5fzTo={n_x} luac={n_l}', flush=True)
    if n_l:
        i = b.find(b'\x1bLuaQ')
        ln = struct.unpack_from('<I', b, i+12)[0]
        src = b[i+16:i+16+ln-1]
        print(f'   首个 luac: {src!r}', flush=True)
    if n_x:
        i = b.find(b'X1V5fzTo')
        print(f'   首个 X1V5fzTo @ {hex(i)}: {b[i:i+40].hex()}', flush=True)
        # 段内 16B 可打印串 (找 key)
        cands = set()
        for m in re.finditer(rb'[\x20-\x7e]{16}', b):
            cands.add(m.group(0)[:16])
        print(f'   可打印 16B 串 {len(cands)} 个:', flush=True)
        for c in list(cands)[:20]:
            print('     ', repr(c), flush=True)
