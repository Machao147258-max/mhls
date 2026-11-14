# -*- coding: utf-8 -*-
"""通过 subprocess 调用 adb, 检查模拟器连接与游戏安装状态"""
import subprocess, sys

ADB = r"D:\MuMuPlayer\nx_main\adb.exe"

def run(args, timeout=60):
    try:
        p = subprocess.run([ADB] + args, capture_output=True, timeout=timeout)
        out = (p.stdout or b'') + (p.stderr or b'')
        return p.returncode, out.decode('utf-8', 'replace')
    except Exception as e:
        return -1, f"ERR {e}"

rc, out = run(["devices"])
print("[devices] rc=", rc)
print(out)

rc, out = run(["shell", "pm", "list", "packages"], timeout=90)
print("[packages] rc=", rc)
if out:
    pkgs = [l for l in out.splitlines() if 'netease' in l.lower() or 'tom' in l.lower()]
    print("matched packages:")
    print("\n".join(pkgs) if pkgs else "(none)")
    print("total lines:", len(out.splitlines()))
else:
    print("(no output)")