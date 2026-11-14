# -*- coding: utf-8 -*-
"""在 libcocos2dlua.so 中定位 OpenSSL 1.0.1c 关键字符串(锚点)，
用于 xref 定位 SSL_read/SSL_write/SSL_connect/SSL_new/SSL_CTX_new 等未导出符号。
"""
import re, struct

SO = r"C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so"
data = open(SO, 'rb').read()
print(f"size: {len(data)}")

# OpenSSL 1.0.1c 关键锚点字符串
anchors = [
    b"SSL_read", b"SSL_write", b"SSL_connect", b"SSL_new", b"SSL_CTX_new",
    b"ssl3_read_bytes", b"ssl3_write_bytes", b"ssl3_read", b"ssl3_write",
    b"ssl23_read", b"ssl23_write", b"SSL_do_handshake", b"ssl3_connect",
    b"ssl3_accept", b"ssl3_get_record", b"tls1_enc", b"ssl3_setup_buffers",
    b"SSL_get_error", b"SSL_pending", b"SSL_CTX_ctrl", b"SSL_ctrl",
    b"SSL_get_fd", b"SSL_set_fd", b"SSL_set_connect_state", b"SSL_clear",
    b"SSL_free", b"SSL_CTX_free", b"SSL_CTX_use_certificate",
    b"SSL_F_SSL_READ", b"SSL_F_SSL_WRITE", b"SSL_F_SSL_CONNECT",
    b"SSL_F_SSL_NEW", b"SSL_F_SSL3_READ_BYTES", b"SSL_F_SSL3_WRITE_BYTES",
    b"SSL_F_SSL_DO_HANDSHAKE", b"SSL_F_SSL3_CONNECT",
    b"ssl3_num_ciphers", b"ssl3_get_cipher", b"SSL_library_init",
    b"SSLv23_client_method", b"TLSv1_client_method", b"TLSv1_1_client_method",
    b"TLSv1_2_client_method", b"SSLv23_method", b"SSL_get_verify_result",
    b"SSL_CTX_set_verify", b"SSL_CTX_set_cert_verify_callback",
    b"SSL_CTX_set_default_verify_paths", b"ssl3_enc", b"ssl3_alert",
    b"SSL_OP_NO_SSLv2", b"SSL_OP_NO_SSLv3", b"SSL_OP_NO_TLSv1",
]

for a in anchors:
    offs = [m.start() for m in re.finditer(re.escape(a), data)]
    if offs:
        # 找到所有偏移，显示前5个
        show = offs[:5]
        print(f"[+] 0x{offs[0]:x} (n={len(offs)}) {a.decode()}")
    else:
        print(f"[-] -- {a.decode()}")

# 额外：找 OpenSSL 版本串与 EVP
for a in [b"OpenSSL 1.0.1c", b"1.0.1c", b"SSLeay", b"built on: ", b"OPENSSLDIR"]:
    offs = [m.start() for m in re.finditer(re.escape(a), data)]
    if offs:
        for o in offs[:3]:
            seg = data[o-16:o+64].replace(b'\x00', b'|')
            print(f"[s] 0x{o:x} {a.decode()} :: {seg[:80]}")