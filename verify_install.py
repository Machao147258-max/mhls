# -*- coding: utf-8 -*-
"""验证安装 + 提取启动 Activity"""
import subprocess
ADB = r"D:\MuMuPlayer\nx_main\adb.exe"
def run(dev, args, timeout=120):
    p = subprocess.run([ADB, "-s", dev] + args, capture_output=True, timeout=timeout)
    return p.returncode, (p.stdout or b'').decode('utf-8','replace'), (p.stderr or b'').decode('utf-8','replace')

dev = "127.0.0.1:7555"
rc, out, err = run(dev, ["shell", "pm", "list", "packages", "|", "grep", "-i", "tom"])
print("pkgs:", out, err)

# 查启动 activity
rc, out, err = run(dev, ["shell", "cmd", "package", "resolve-activity", "--brief", "com.netease.tom", "|", "tail", "-1"])
print("resolve:", out.strip(), err.strip())

# lib 架构确认 (apk 里有什么 so 不重要, 运行时抓)
rc, out, err = run(dev, ["shell", "pm", "path", "com.netease.tom"])
print("path:", out.strip(), err.strip())