# -*- coding: utf-8 -*-
"""用 su 检查游戏包安装 + frida-server 状态"""
import subprocess

ADB = r"D:\MuMuPlayer\nx_main\adb.exe"

def run(dev, args, timeout=120):
    try:
        p = subprocess.run([ADB, "-s", dev] + args, capture_output=True, timeout=timeout)
        return p.returncode, (p.stdout or b'').decode('utf-8', 'replace'), (p.stderr or b'').decode('utf-8', 'replace')
    except Exception as e:
        return -1, "", str(e)

devs = ["127.0.0.1:7555", "emulator-5556", "emulator-5558"]
for d in devs:
    print(f"===== {d} =====")
    # 游戏包(用 su 执行pm)
    rc, out, err = run(d, ["shell", "su", "-c", "pm list packages"], 180)
    pkgs = [l for l in out.splitlines() if ('netease' in l.lower() or 'tom' in l.lower())]
    print(f"  netease/tom packages: {pkgs if pkgs else '(none)'}")
    # frida-server 进程
    rc, out, err = run(d, ["shell", "ps", "-A"], 60)
    fr = [l for l in out.splitlines() if 'frida' in l.lower()]
    print(f"  frida procs: {fr if fr else '(none)'}")
    # /data/local/tmp 中 frida-server
    rc, out, err = run(d, ["shell", "ls", "/data/local/tmp/"], 60)
    fs = [l for l in out.splitlines() if 'frida' in l.lower() or 'cacert' in l.lower() or '.so' in l.lower()]
    print(f"  frida/cacert files: {fs if fs else '(none)'}")
    print()