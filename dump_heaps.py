# -*- coding: utf-8 -*-
# 批量抓取大匿名段 → 本地搜默认 key → 定位 XXTEAUtil
import subprocess, os, re, struct

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
pid = '18380'
SEGS = [
    ('0x778e90600000', '0x778e9c600000', 'heap192'),
    ('0x778f6a75d000', '0x778f6c7dd000', 'heap32'),
    ('0x778e2ebb3000', '0x778e306db000', 'heap27'),
    ('0x778f4a70e000', '0x778f4c18e000', 'heap26'),
    ('0x778e31376000', '0x778e329a5000', 'heap22'),
    ('0x778e2c800000', '0x778e2da19000', 'heap18'),
]
KEY1 = bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b')
os.makedirs(r'C:\Users\20751\tomdump\live_heap', exist_ok=True)

def sh(a, t=300):
    r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + a, capture_output=True, timeout=t)
    return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()

for s, e, name in SEGS:
    start, end = int(s, 16), int(e, 16)
    total = (end - start + 4095) >> 12
    dev = f'/data/local/tmp/h_{name}.bin'
    sh(['shell', f'su -c "rm -f {dev}"'])
    done = 0
    chunk = (8 << 20) >> 12
    while done < total:
        n = min(chunk, total - done)
        r = sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={(start>>12)+done} count={n} of={dev}.{done>>11} 2>&1"'], t=300)
        done += n
        print(f'{name}: {done}/{total} 页', flush=True)
    sh(['shell', f'su -c "cat {dev}.* > {dev} 2>/dev/null; rm -f {dev}.*"'])
    sh(['pull', dev, rf'C:\Users\20751\tomdump\live_heap\{name}.bin'], t=600)
    b = open(rf'C:\Users\20751\tomdump\live_heap\{name}.bin', 'rb').read()
    i = b.find(KEY1)
    print(f'{name}: {len(b)}B KEY1 @ {hex(i) if i>=0 else "NO"}', flush=True)
    if i >= 0:
        print(f'  ctx: {b[max(0,i-64):i+96].hex()}', flush=True)
