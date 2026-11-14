# -*- coding: utf-8 -*-
"""解析 libcocos2dlua.so 的 SSL3_ENC_METHOD 实例 (TLSv1_enc_data 等), 获取真实 ssl3_* 函数地址锚点"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

# 候选: 从符号表找 *_enc_data / *_method / enc_method 对象
import subprocess
r = subprocess.run(['readelf','-Ws',F], capture_output=True, timeout=180)
txt = (r.stdout or b'').decode('utf-8','replace')
lines = txt.splitlines()

objs = []
for ln in lines:
    import re
    m = re.match(r'\s*\d+:\s+([0-9a-f]{16})\s+(\d+)\s+(\S+)\s+GLOBAL\s+DEFAULT\s+(\d+)\s+(.*)$', ln)
    if m:
        val, size, typ, ndx, name = m.groups()
        name = name.strip()
        if typ == 'OBJECT' and (name.endswith('enc_data') or name.endswith('_method')
                                or 'enc_method' in name or 'finished_label' in name):
            objs.append((int(val,16), int(size), name))
            print(f"OBJECT {name:48s} @ {hex(int(val,16))} (size {size})")

# SSL3_ENC_METHOD (1.0.1c) qword layout:
# [0]enc [1]mac [2]setup_key_block [3]generate_master_secret [4]change_cipher_state
# [5]final_finish_mac [6]cert_verify_mac [7]client_finished_label* [8]len [9]server_finished_label* [10]len [11]alert_suffix
names = ['ssl3_enc','ssl3_mac','ssl3_setup_key_block','ssl3_generate_master_secret',
         'ssl3_change_cipher_state','ssl3_final_finish_mac','ssl3_cert_verify_mac',
         'client_finished_label','cfl_len','server_finished_label','sfl_len','alert_suffix']

print("\n=== SSL3_ENC_METHOD 表解析 ===")
for val, size, nm in objs:
    if size < 0x60:
        continue
    off = v2off(val)
    nq = min(size // 8, 14)
    q = struct.unpack_from(f'<{nq}Q', d, off)
    print(f"\n--- {nm} @ {hex(val)} (size {size}) ---")
    for i, v in enumerate(q):
        label = names[i] if i < len(names) else f'q{i}'
        if i in (7,9) and v:  # label ptr -> show string
            lo = v2off(v)
            s = d[lo:lo+40]
            s = s.split(b'\x00')[0].decode('ascii','replace')
            print(f"  [{i:2d}] {label:28s} = {hex(v)}  ('{s}')")
        else:
            print(f"  [{i:2d}] {label:28s} = {hex(v)}")