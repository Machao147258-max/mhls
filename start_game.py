# -*- coding: utf-8 -*-
"""启动游戏并确认进程"""
import subprocess, time, sys
ADB = r"D:\MuMuPlayer\nx_main\adb.exe"
def run(dev, args, timeout=120):
    p = subprocess.run([ADB, "-s", dev] + args, capture_output=True, timeout=timeout)
    return p.returncode, (p.stdout or b'').decode('utf-8','replace'), (p.stderr or b'').decode('utf-8','replace')

dev = "127.0.0.1:7555"
# 启动游戏
rc, out, err = run(dev, ["shell", "am", "start", "-n", "com.netease.tom/com.netease.ntunisdk.external.protocol.ProtocolLauncher"])
print("[am start]", rc, out.strip()[:300], err.strip()[:100])

# 等待进程出现
for i in range(30):
    rc, out, err = run(dev, ["shell", "pidof", "com.netease.tom"])
    pid = out.strip()
    if pid:
        print(f"[pidof] com.netease.tom PID={pid} after {i*2}s")
        break
    time.sleep(2)
else:
    print("[pidof] NOT FOUND within 60s")
    rc, out, err = run(dev, ["shell", "ps", "-A"])
    lines = [l for l in out.splitlines() if 'tom' in l.lower() or 'netease' in l.lower()]
    print("related:", lines[:10])