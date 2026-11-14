# -*- coding: utf-8 -*-
"""检查 objdump 是否支持 aarch64 + 定位可用的反汇编工具"""
import subprocess, shutil, os

cands = ["objdump", "C:/mingw64/bin/objdump.exe", "C:/msys64/mingw64/bin/objdump.exe",
         "C:/Program Files/Git/usr/bin/objdump.exe", "llvm-objdump", "llvm-objdump-17",
         "aarch64-linux-gnu-objdump", "arm-linux-androideabi-objdump"]

for c in cands:
    p = shutil.which(c)
    if p:
        try:
            r = subprocess.run([p, "-i"], capture_output=True, timeout=30)
            out = (r.stdout or b'').decode('utf-8', 'replace') + (r.stderr or b'').decode('utf-8', 'replace')
            has_aarch64 = 'aarch64' in out.lower() or 'arm' in out.lower()
            has_x86 = 'i386' in out.lower() or 'x86-64' in out.lower()
            print(f"[FOUND] {c} -> {p}")
            print(f"   aarch64={'aarch64' in out.lower()}  x86={'i386' in out.lower() or 'x86-64' in out.lower()}")
            print(f"   head: {out[:200].strip()}")
        except Exception as e:
            print(f"[{c}] ERR {e}")
    else:
        print(f"[missing] {c}")