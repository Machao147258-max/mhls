# -*- coding: utf-8 -*-
"""adb 环境探测: shell 可用性、Android 版本、root、游戏包"""
import subprocess

ADB = r"D:\MuMuPlayer\nx_main\adb.exe"

def run(args, timeout=90):
    try:
        p = subprocess.run([ADB] + args, capture_output=True, timeout=timeout)
        return p.returncode, (p.stdout or b'').decode('utf-8', 'replace'), (p.stderr or b'').decode('utf-8', 'replace')
    except Exception as e:
        return -1, "", str(e)

# 对每个设备测试
devs = ["127.0.0.1:7555", "emulator-5556", "emulator-5558"]
for d in devs:
    print(f"===== {d} =====")
    for cmd in [["shell", "echo", "hello_ok"],
                ["shell", "getprop", "ro.product.model"],
                ["shell", "getprop", "ro.build.version.release"],
                ["shell", "whoami"],
                ["shell", "id"]]:
        rc, out, err = run(["-s", d] + cmd)
        status = "OK" if rc == 0 else f"RC={rc}"
        print(f"  [{status}] {' '.join(cmd)} -> {out.strip()[:80]}{err.strip()[:80]}")
    # root 检查
    rc, out, err = run(["-s", d, "shell", "su", "-c", "id"])
    print(f"  [su] -> {out.strip()[:80]}{err.strip()[:80]}")
    # frida 检查
    rc, out, err = run(["-s", d, "shell", "ls", "/data/local/tmp/"])
    print(f"  [/data/local/tmp] -> {out.strip()[:200]}{err.strip()[:80]}")
    print()