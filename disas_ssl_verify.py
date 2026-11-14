# -*- coding: utf-8 -*-
"""反汇编 libAudioCommon.so 关键 SSL 校验函数 (arm64)"""
import subprocess, os

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libAudioCommon.so"
BIN = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib"

# 目标: 函数名 -> (偏移, 大小)
targets = {
    "X509_verify_cert":        (0x2a2dd4, 868),
    "ssl_verify_cert_chain":   (0x212894, 584),
    "tls_process_server_cert": (0x22b450, 1204),
    "ssl3_check_cert_and_alg": (0x22cdec, 240),
    "SSL_CTX_set_verify":      (0x21bba8, 12),
    "SSL_CTX_set_cert_verify_callback": (0x21bba0, 8),
}

# mingw 里 objdump 名称探测
import shutil
objdump = None
for cand in [r"C:\msys64\mingw64\bin\objdump.exe", r"C:\Program Files\Git\usr\bin\objdump.exe", "objdump"]:
    p = shutil.which(cand) if not os.path.isabs(cand) else (cand if os.path.exists(cand) else None)
    if p:
        objdump = p
        break
print("objdump =", objdump)

for name, (off, size) in targets.items():
    out = subprocess.run([objdump, "-d", "--start-address=0x%x" % off,
                          "--stop-address=0x%x" % (off + size), SO],
                         capture_output=True, timeout=120)
    txt = out.stdout.decode('utf-8', 'replace')
    # 只保留指令行
    lines = [l for l in txt.splitlines() if '\t' in l]
    print(f"\n===== {name} @ 0x{off:x} (+{size}) =====")
    print("\n".join(lines[:80]))