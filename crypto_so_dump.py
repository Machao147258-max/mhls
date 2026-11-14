# -*- coding: utf-8 -*-
# 设备端脚本抓 so 内存 (复用 mega_dump 成功模式)
import subprocess, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
D = '127.0.0.1:16416'
PID = '6894'

def sh(args, t=600):
    r = subprocess.run([ADB, '-s', D] + args, capture_output=True, timeout=t)
    return r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')

# 抓整个 so 映射: 0x400020e00000 - 0x400022640000 (0x1840000 = 25427968B)
BASE = 0x400020e00000
SIZE = 0x1840000
script = f'''#!/system/bin/sh
cd /data/local/tmp
rm -f mem_so.bin
dd if=/proc/{PID}/mem bs=4096 skip=$(({BASE}/4096)) count=$(({SIZE}/4096)) of=mem_so.bin 2>/dev/null
ls -l mem_so.bin
'''
open(r'C:\Users\20751\tomdump\sodump.sh', 'w', newline='\n').write(script)
print('push...')
print(sh(['push', r'C:\Users\20751\tomdump\sodump.sh', '/data/local/tmp/sodump.sh'])[:80])
print('exec...')
print(sh(['shell', 'su -c sh /data/local/tmp/sodump.sh'], t=900)[-150:])
print('pull...')
print(sh(['pull', '/data/local/tmp/mem_so.bin', r'C:\Users\20751\tomdump\mem_so.bin'], t=900)[:80])
sz = os.path.getsize(r'C:\Users\20751\tomdump\mem_so.bin') if os.path.exists(r'C:\Users\20751\tomdump\mem_so.bin') else 0
print(f'mem_so.bin: {sz/1024/1024:.1f}MB')