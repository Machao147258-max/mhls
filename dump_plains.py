# -*- coding: utf-8 -*-
"""dump_plains.py — dump 明文 luac 完整内容到 PC
用法: python dump_plains.py <pid>
"""
import subprocess, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
PID = '20113'
OUT = r'C:\Users\20751\Desktop\猫和老鼠\PLAINS'
os.makedirs(OUT, exist_ok=True)

# (src_addr, size, 标注)
targets = [
    (0x72b5cf9e15f8, 248396, 's1_248396'),
    (0x72b5cf9e1abc, 249412, 's2_249412'),
    (0x72b5cfeb9c1c, 154636, 's3_154636'),
    (0x72b5d04c29d4, 123920, 's4_123920'),
    (0x72b5d04c30c0, 119116, 's5_119116'),
    (0x72b5d04c46e0, 113964, 's6_113964'),
    (0x72b5d04c4d08, 114028, 's7_114028'),
]

for addr, size, name in targets:
    dev = f'/data/local/tmp/{name}.bin'
    # dd 到设备文件 (bs=1 太慢; 用 bs=4096 对齐)
    base = addr & ~0xFFF
    off = addr - base
    blocks = (off + size + 4095) // 4096
    r = subprocess.run(
        [ADB, '-s', '127.0.0.1:7555', 'shell', 'su', '-c',
         f'dd if=/proc/{PID}/mem bs=4096 skip=$(({base}>>12)) count={blocks} 2>/dev/null | dd bs=1 skip={off} count={size} > {dev} 2>/dev/null'],
        capture_output=True, text=True, timeout=120)
    # pull
    r2 = subprocess.run([ADB, '-s', '127.0.0.1:7555', 'pull', dev, os.path.join(OUT, f'{name}.bin')],
                        capture_output=True, text=True, timeout=60)
    size_pc = os.path.getsize(os.path.join(OUT, f'{name}.bin')) if os.path.exists(os.path.join(OUT, f'{name}.bin')) else 0
    # 检查头
    if size_pc > 8:
        with open(os.path.join(OUT, f'{name}.bin'), 'rb') as f:
            head = f.read(16).hex()
        print(f'{name}: pulled {size_pc}B head={head}')
    else:
        print(f'{name}: FAIL ({size_pc}B)')
print('DONE')