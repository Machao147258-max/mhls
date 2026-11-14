# -*- coding: utf-8 -*-
"""查所有 tom_lib so 中 UND 引用的 SSL 符号 -> 找出真正的 SSL 使用方"""
import os, subprocess, re

DIR = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib"
ssl_und = ["SSL_CTX_new", "SSL_new", "SSL_read", "SSL_write", "SSL_connect",
           "SSL_do_handshake", "SSL_CTX_set_verify", "BIO_new", "BIO_read", "BIO_write"]

for fn in sorted(os.listdir(DIR)):
    if not fn.endswith('.so'):
        continue
    p = os.path.join(DIR, fn)
    r = subprocess.run(["readelf", "-Ws", p], capture_output=True, timeout=120)
    txt = (r.stdout or b'').decode('utf-8', 'replace')
    found = []
    for ln in txt.splitlines():
        if 'UND' in ln:
            for s in ssl_und:
                # 明文 UND 符号行 (libAudioCommon 未混淆; 混淆库无 UND 明文但可能引用)
                if re.search(r'\b' + s + r'\b', ln):
                    found.append(s)
                    break
    if found:
        # 去重保序
        seen = []
        for s in found:
            if s not in seen:
                seen.append(s)
        print(f"{fn:32s} UND-SSL: {', '.join(seen)}")