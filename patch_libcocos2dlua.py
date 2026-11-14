# -*- coding: utf-8 -*-
"""幂等 patch: libcocos2dlua.so (OpenSSL 1.0.1c ARM64)
X509_verify_cert @ 0xbc5e4c -> mov w0,#1; ret"""
import struct, shutil, os

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
BAK = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so.orig'
TGT = 0xbc5e4c
PATCH = bytes.fromhex('20 00 80 52 C0 03 5F D6')
ORIG  = bytes.fromhex('FD 7B B7 A9 FD 03 00 91')

d = bytearray(open(F, 'rb').read())
cur = bytes(d[TGT:TGT+8])
print(f"offset 0x{TGT:x} current 8B: {cur.hex(' ')}")

if cur == PATCH:
    print("[OK] already patched (idempotent)")
elif cur == ORIG:
    if not os.path.exists(BAK):
        shutil.copy2(F, BAK)
        print(f"backup -> {BAK}")
    d[TGT:TGT+8] = PATCH
    open(F, 'wb').write(bytes(d))
    got = open(F, 'rb').read()[TGT:TGT+8]
    print(f"[OK] patched -> {got.hex(' ')}  {'MATCH' if got == PATCH else 'FAIL'}")
else:
    print(f"[ABORT] unexpected bytes, no change. (patch/backup untouched)")

# restore script
rp = r'C:\Users\20751\Desktop\猫和老鼠\restore_libcocos2dlua.py'
open(rp, 'w', encoding='utf-8').write(f'''import shutil, os
BAK = r'{BAK}'
F = r'{F}'
if os.path.exists(BAK):
    shutil.copy2(BAK, F)
    print("restored")
else:
    print("no backup")
''')
print(f"restore script: {rp}")