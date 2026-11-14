# -*- coding: utf-8 -*-
"""探测 emulator-5556 架构 + 游戏安装状态"""
import subprocess
ADB = r"D:\MuMuPlayer\nx_main\adb.exe"
def run(dev, args, timeout=120):
    p = subprocess.run([ADB, "-s", dev] + args, capture_output=True, timeout=timeout)
    return p.returncode, (p.stdout or b'').decode('utf-8','replace'), (p.stderr or b'').decode('utf-8','replace')

d = "emulator-5556"
for cmd in [["shell","getprop","ro.product.cpu.abilist"],
            ["shell","getprop","ro.product.cpu.abi"],
            ["shell","getprop","ro.build.ab_update"],
            ["shell","uname","-m"],
            ["shell","su","-c","pm list packages"] ]:
    rc, out, err = run(d, cmd)
    pkgs = [l for l in out.splitlines() if ('netease' in l.lower() or 'tom' in l.lower())]
    print(f"[{' '.join(cmd)}] rc={rc} :: {out.strip()[:200]}")
    if pkgs:
        print("   PKG:", pkgs)
    if err.strip():
        print("   ERR:", err.strip()[:200])