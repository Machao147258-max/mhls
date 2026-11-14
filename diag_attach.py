# -*- coding: utf-8 -*-
"""诊断: 进程状态 + frida 列表"""
import subprocess, frida, time
ADB = r"D:\MuMuPlayer\nx_main\adb.exe"
def run(args, timeout=60):
    p = subprocess.run([ADB, "-s", "127.0.0.1:7555"] + args, capture_output=True, timeout=timeout)
    return p.returncode, (p.stdout or b'').decode('utf-8','replace'), (p.stderr or b'').decode('utf-8','replace')

# 1) 进程还活着吗
rc, out, err = run(["shell", "ps", "-A", "|", "grep", "tom"])
print("[ps]", out.strip()[:300])

# 2) 进程 maps 架构判断 - 看它加载的 so 路径 (arm64 vs x86_64)
rc, out, err = run(["shell", "cat", "/proc/52554/maps", "|", "grep", "-E", "libcocos2dlua|libAudioCommon|secsdk|libunisec", "|", "head", "-20"])
print("[maps ssl/cocos]")
print(out.strip()[:1500])

# 3) frida 能列出进程吗
try:
    dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
    procs = dev.enumerate_processes()
    toms = [p for p in procs if 'tom' in (p.name or '').lower() or 'netease' in (p.name or '').lower()]
    print("[frida procs] total", len(procs))
    for p in toms[:10]:
        print("   ", p.pid, p.name)
except Exception as e:
    print("[frida enum fail]", e)