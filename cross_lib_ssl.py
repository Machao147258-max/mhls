# -*- coding: utf-8 -*-
"""跨库确认: ① 字节级搜索 SSL_CTX_new/SSL_read/SSL_write 的明文符号/字符串
   ② readelf -d NEEDED 依赖
   ③ libcocos2dlua.so 是否有 SSL_CTX_new 的 UND (混淆名)"""
import os, subprocess, re, struct

DIR = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib"
SO = os.path.join(DIR, "libAudioCommon.so")

needles = [b"SSL_CTX_new", b"SSL_read", b"SSL_write", b"X509_verify_cert", b"SSL_connect", b"SSL_do_handshake"]

print("=== 字节级符号/字符串搜索 ===")
for fn in sorted(os.listdir(DIR)):
    if not fn.endswith('.so'):
        continue
    p = os.path.join(DIR, fn)
    d = open(p, 'rb').read()
    hits = []
    for n in needles:
        c = d.count(n)
        if c:
            # 找第一个出现位置 vs 是否为符号表名 (GLOBAL FUNC)
            hits.append(f"{n.decode()}={c}")
    if hits:
        print(f"{fn:32s} {'; '.join(hits)}")

print("\n=== libAudioCommon.so NEEDED ===")
r = subprocess.run(["readelf", "-d", SO], capture_output=True, timeout=60)
for ln in (r.stdout or b'').decode('utf-8','replace').splitlines():
    if 'NEEDED' in ln:
        print(" ", ln.strip()[ln.strip().find('('):])

print("\n=== libcocos2dlua.so 的 SSL UND 符号 (混淆名) ===")
p = os.path.join(DIR, "libcocos2dlua.so")
r = subprocess.run(["readelf", "-Ws", p], capture_output=True, timeout=120)
txt = (r.stdout or b'').decode('utf-8','replace')
cnt = 0
for ln in txt.splitlines():
    if 'UND' in ln and ('SSL_read' in ln or 'SSL_write' in ln or 'SSL_CTX_new' in ln or 'SSL_connect' in ln or 'SSL' in ln and 'FUNC' in ln):
        print(" ", ln.strip()[:170])
        cnt += 1
        if cnt > 40:
            break
if cnt == 0:
    print("  (未见明文 SSL UND——符号名被混淆, 需字节级确认)")

print("\n=== secsdk/libunisec NEEDED (易盾栈依赖) ===")
for fn in ["secsdk.so", "libunisec.so", "libsec-lib.so"]:
    p2 = os.path.join(DIR, fn)
    if not os.path.exists(p2):
        p2 = os.path.join(r"C:\Users\20751\Desktop\猫和老鼠", fn)
    if not os.path.exists(p2):
        continue
    r = subprocess.run(["readelf", "-d", p2], capture_output=True, timeout=60)
    need = [ln.strip()[ln.strip().find('['):] for ln in (r.stdout or b'').decode('utf-8','replace').splitlines() if 'NEEDED' in ln]
    print(f"{fn}: {', '.join(need)}")