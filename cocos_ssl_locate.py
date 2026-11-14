# -*- coding: utf-8 -*-
"""① 在 libcocos2dlua.so (1.0.1c) 字节级定位核心 SSL 校验/IO 函数 (符号混淆, 用 .dynstr 明文)
   ② 检查 libNgModules/libybuaxz/libntunisdk/libsec-lib 的 TLS 特征"""
import os, subprocess, re, struct

DIR = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib"
COCOS = os.path.join(DIR, "libcocos2dlua.so")
d = open(COCOS, 'rb').read()
print("libcocos2dlua.so size:", len(d))

# 1) 用 .dynstr 明文符号名 -> 地址: readelf -Ws 全表 (混淆名后跟明文, 但符号表记录着混淆名)
#    更可靠: 解析 .dynsym, 符号名 offset -> .dynstr, 但 section 头剥离.
#    用 readelf -Ws 输出: "混淆名 SSL_read" 模式提取
r = subprocess.run(["readelf", "-Ws", COCOS], capture_output=True, timeout=180)
txt = (r.stdout or b'').decode('utf-8','replace')
lines = txt.splitlines()

want = ["SSL_read", "SSL_write", "SSL_connect", "SSL_CTX_new", "SSL_new",
        "SSL_do_handshake", "X509_verify_cert", "ssl_verify_cert_chain",
        "ssl3_check_cert_and_algorithm", "SSL_CTX_set_verify", "SSL_get_verify_result",
        "ssl3_read_bytes", "ssl3_write_bytes", "ssl3_get_server_certificate"]

# 符号行格式: "Num: Value Size Type Bind Vis Ndx Name"
# 混淆名形如 "<95><CF>...<FF>SSL_read" (plain suffix visible)
found = {}
for ln in lines:
    m = re.match(r'\s*\d+:\s+([0-9a-f]{16})\s+(\d+)\s+(\S+)\s+GLOBAL\s+DEFAULT\s+(\d+)\s+(.*)$', ln)
    if m:
        val, size, typ, ndx, name = m.groups()
        name = name.strip()
        for w in want:
            # 混淆名以明文结尾 (前面可能有 .note.gnu.build-id 或直接混淆前缀)
            if name.endswith(w) and typ == 'FUNC':
                found[w] = (int(val, 16), int(size))
                break
print("\n=== libcocos2dlua.so (OpenSSL 1.0.1c) 核心符号 ===")
for w in want:
    if w in found:
        v, s = found[w]
        print(f"  {w:38s} @ 0x{v:x} (size {s})")
    else:
        print(f"  {w:38s} -- NOT FOUND")

# 2) 其余 so TLS 特征
print("\n=== 其余 so TLS 特征 ===")
for fn in ["libNgModules.so", "libybuaxz.so", "libntunisdk.so", "libsec-lib.so", "libunisec.so"]:
    for root2 in [DIR, r"C:\Users\20751\Desktop\猫和老鼠"]:
        p = os.path.join(root2, fn)
        if os.path.exists(p):
            break
    if not os.path.exists(p):
        print(f"{fn}: missing")
        continue
    dd = open(p, 'rb').read()
    probes = {
        "OpenSSL": dd.count(b"OpenSSL"), "BoringSSL": dd.count(b"BoringSSL"),
        "libssl": dd.count(b"libssl"), "SSL_read": dd.count(b"SSL_read"),
        "BEGIN CERT": dd.count(b"-----BEGIN CERT"), "TLS1.3": dd.count(b"TLS 1.3"),
        "GmSSL": dd.count(b"GmSSL"), "keylog": dd.count(b"keylog"),
        "pinning": dd.count(b"pinning") + dd.count(b"Pinning"),
        "x509": dd.count(b"X509_") + dd.count(b"x509"),
    }
    hit = {k: v for k, v in probes.items() if v}
    # NEEDED
    r = subprocess.run(["readelf", "-d", p], capture_output=True, timeout=60)
    need = [ln.strip()[:110] for ln in (r.stdout or b'').decode('utf-8','replace').splitlines() if 'NEEDED' in ln]
    print(f"{fn}: size={len(dd)} {hit if hit else '(无TLS特征)'}")
    for n in need:
        print(f"    {n}")