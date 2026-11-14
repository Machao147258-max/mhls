# -*- coding: utf-8 -*-
"""重装 device_base.apk 到 127.0.0.1:7555 模拟器 (长超时)"""
import subprocess, time, sys

ADB = r"D:\MuMuPlayer\nx_main\adb.exe"
APK = r"C:\Users\20751\Desktop\猫和老鼠\device_base.apk"
DEV = "127.0.0.1:7555"

t0 = time.time()
print(f"[*] installing {APK} -> {DEV}  (this may take several minutes)", flush=True)
try:
    p = subprocess.run([ADB, "-s", DEV, "install", "-r", "-t", "-d", APK],
                       capture_output=True, timeout=1500)
    out = (p.stdout or b'').decode('utf-8', 'replace')
    err = (p.stderr or b'').decode('utf-8', 'replace')
    print(f"[*] rc={p.returncode}  elapsed={time.time()-t0:.0f}s")
    print("STDOUT:", out[-2000:] if out else "(none)")
    print("STDERR:", err[-2000:] if err else "(none)")
except Exception as e:
    print(f"[!] EXC {e}")