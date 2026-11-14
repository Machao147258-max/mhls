# -*- coding: utf-8 -*-
"""检查 frida-server 监听端口 + 本机 frida 客户端可用性"""
import subprocess, sys
ADB = r"D:\MuMuPlayer\nx_main\adb.exe"
def run(args, timeout=60):
    p = subprocess.run([ADB, "-s", "127.0.0.1:7555"] + args, capture_output=True, timeout=timeout)
    return p.returncode, (p.stdout or b'').decode('utf-8','replace'), (p.stderr or b'').decode('utf-8','replace')

# frida-server 监听端口
rc, out, err = run(["shell", "netstat", "-tlnp", "|", "grep", "frida"])
print("[frida ports]", out.strip()[:300], err.strip()[:100])

# 本地 frida 客户端
try:
    import frida
    print("[local frida]", frida.__version__)
except Exception as e:
    print("[local frida] NOT AVAILABLE:", e)

# 测试连接设备
try:
    dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")
    print("[remote device]", dev)
    print("[params]", dev.query_system_parameters())
except Exception as e:
    print("[remote connect] FAIL:", e)