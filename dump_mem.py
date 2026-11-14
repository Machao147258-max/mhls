# -*- coding: utf-8 -*-
# 通用内存抓取: dd 分页抓 /proc/PID/mem 区间 → 设备临时文件 → pull
# 用法: python dump_mem.py <pid> <start_hex> <size_hex> <名称>
import subprocess, sys, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
pid, start, size, name = sys.argv[1], int(sys.argv[2], 16), int(sys.argv[3], 16), sys.argv[4]

def sh(a, t=120):
    r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + a, capture_output=True, timeout=t)
    return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()

dev_path = f'/data/local/tmp/dump_{name}.bin'
local_path = rf'C:\Users\20751\tomdump\mem_{name}.bin'

# 分块抓 (每块 8MB, 避免 dd 单次太大)
page = start >> 12
total_pages = (size + 4095) >> 12
chunk_pages = (8 << 20) >> 12
print(f'PID {pid} {name}: start=0x{start:x} size=0x{size:x} ({size/1048576:.1f}MB) 页数={total_pages}', flush=True)
sh(['shell', f'su -c "rm -f {dev_path}"'])
done = 0
while done < total_pages:
    n = min(chunk_pages, total_pages - done)
    part = f'{dev_path}.{done >> 11}'
    r = sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page+done} count={n} of={part} 2>&1"'], t=300)
    if 'error' in r.lower() and 'records' not in r:
        print('  读取错误:', r[:200], flush=True)
        break
    done += n
    print(f'  ...{done}/{total_pages} 页', flush=True)
# 合并
sh(['shell', f'su -c "cat {dev_path}.* > {dev_path} 2>/dev/null; rm -f {dev_path}.*"'])
r = sh(['shell', f'su -c "ls -la {dev_path}"'])
print('设备文件:', r, flush=True)
r = sh(['pull', dev_path, local_path], t=600)
print('pull:', r[:100], flush=True)
sz = os.path.getsize(local_path) if os.path.exists(local_path) else 0
print(f'本地: {local_path} {sz} 字节', flush=True)
