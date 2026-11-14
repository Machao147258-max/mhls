# -*- coding: utf-8 -*-
"""read_dst.py — 用 dd 分块读 /proc/<pid>/mem 的指定地址 (64 位 offset 兼容)
用法: python read_dst.py <pid> <hexaddr> <bytes>
"""
import sys, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
PID, ADDR, N = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3])

# dd bs=1 太慢; 用 bs=4096 对齐块读
base = ADDR & ~0xFFF
off = ADDR - base
blocks = (off + N + 4095) // 4096

r = subprocess.run(
    [ADB, 'shell', 'su', '-c',
     f'dd if=/proc/{PID}/mem bs=4096 skip=$(({base}>>12)) count={blocks} 2>/dev/null | xxd -p'],
    capture_output=True, text=True, timeout=60)
raw = r.stdout.replace('\n', '').replace(' ', '')
# xxd -p 输出连续 hex, 截取目标
if not raw:
    print('EMPTY (read failed)')
    sys.exit(1)
hexstr = raw[off * 2: (off + N) * 2]
print('OFFSET', hex(ADDR))
print('HEX:', hexstr[:256])
# ascii
byts = bytes.fromhex(hexstr[: (N if N < 64 else 64) * 2])
print('ASCII:', ''.join(chr(b) if 31 < b < 127 else '.' for b in byts))
