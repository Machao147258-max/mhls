# -*- coding: utf-8 -*-
"""batch_read_mem.py — 用 dd bs=1 读多个地址 (64 位 offset), 找明文
用法: python batch_read_mem.py <pid> <addr1> <addr2> ...
"""
import sys, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
PID = sys.argv[1]
addrs = [int(a, 16) for a in sys.argv[2:]]

for addr in addrs:
    r = subprocess.run(
        [ADB, '-s', '127.0.0.1:7555', 'shell', 'su', '-c',
         f'dd if=/proc/{PID}/mem bs=1 skip={addr} count=16 2>/dev/null | xxd -p'],
        capture_output=True, text=True, timeout=60)
    hexs = r.stdout.strip().replace('\n', '').replace(' ', '')
    if len(hexs) >= 8:
        head = hexs[:8]
        # 明文特征: 非 X1V5fzTo (58315635667a546f)
        is_cipher = head == '58315635'
        if not is_cipher and head != '00000000':
            print(f'★PLAIN {addr:#x}: {head}...')
        elif head != '00000000':
            print(f'cipher {addr:#x}: {head}')
    else:
        print(f'{addr:#x}: n/a')
print('DONE')