# -*- coding: utf-8 -*-
"""检查 7555 模拟器存储空间"""
import subprocess
ADB = r"D:\MuMuPlayer\nx_main\adb.exe"
def run(args, timeout=60):
    p = subprocess.run([ADB, "-s", "127.0.0.1:7555"] + args, capture_output=True, timeout=timeout)
    return p.returncode, (p.stdout or b'').decode('utf-8','replace'), (p.stderr or b'').decode('utf-8','replace')
for cmd in [["shell","df","-h","/data"], ["shell","getprop","ro.product.cpu.abilist"]]:
    rc, out, err = run(cmd)
    print(f"[{' '.join(cmd)}] rc={rc}")
    print(out[:500])