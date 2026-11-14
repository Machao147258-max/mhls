# -*- coding: utf-8 -*-
"""验证 SSL3_ENC_METHOD 实例内容 + 全文件反查 SSL_METHOD 表"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

def off2v(o):
    if 0 <= o < 0x10022b8: return o
    if 0x1002e08 <= o < 0x1580540: return o + 0x10000
    if 0x1574000 <= o < 0x1906000: return o + 0x3d000
    return None
def v2off(v):
    if 0x0 <= v < 0x10022b8: return v
    if 0x1012e08 <= v < 0x1580540: return v - 0x10000
    if 0x15b1000 <= v < 0x1906000: return v - 0x3d000
    return None

EXEC = lambda v: (0x0 <= v < 0x10022b8) or (0x15b1000 <= v < 0x1906000)

# 1) 验证实例
insts = [0x3ad708, 0x3b0990]
labels = ['ssl3_enc','ssl3_mac','setup_kb','gen_master','change_cs','final_finish','cert_verify',
          'client_label','cfl_len','server_label','sfl_len','alert_suffix']
for inst in insts:
    o = v2off(inst)
    qs = struct.unpack_from('<12Q', d, o)
    print(f"=== SSL3_ENC_METHOD 实例 @ {inst:#x} ===")
    for i, q in enumerate(qs):
        extra = ''
        if i in (7, 9) and q:
            lo = v2off(q)
            extra = f"  -> '{d[lo:lo+24].split(b'\\x00')[0].decode('ascii','replace')}'"
        execmark = 'EXEC' if EXEC(q) else ('DATA' if q >= 0x1012e08 else '???')
        print(f"  [{i:2d}] {labels[i]:16s} = {q:#x} {execmark}{extra}")

# 2) 全文件反查引用实例的 qword (方法表 [23]=ssl3_enc)
print("\n=== 反查 SSL_METHOD 表 (引用实例的 qword) ===")
import sys
lim = len(d)  # 到文件尾
found_tables = []
for inst in insts:
    for o in range(0, lim, 8):
        q = struct.unpack_from('<Q', d, o)[0]
        if q != inst:
            continue
        # 候选表基址 = 引用位置 - 23*8
        refv = off2v(o)
        tbl = refv - 23*8
        if tbl < 0 or v2off(tbl) is None:
            continue
        qs = struct.unpack_from('<26Q', d, v2off(tbl))
        # 方法表验证: version 低32位合理 + 指针模式
        ver = qs[0] & 0xFFFFFFFF
        ok = (ver in (0x300, 0x301, 0x302, 0x303, 0xffff)) and EXEC(qs[4]) and EXEC(qs[5]) \
             and EXEC(qs[6]) and EXEC(qs[8]) and EXEC(qs[21]) and EXEC(qs[22])
        mark = '<<<< METHOD TABLE' if ok else ''
        print(f"  引用 {inst:#x} @ {refv:#x} -> 表候选 {tbl:#x} version={ver:#x} {mark}")
        if ok:
            found_tables.append(tbl)
            print(f"       accept={qs[4]:#x} connect={qs[5]:#x} read={qs[6]:#x} peek={qs[7]:#x} write={qs[8]:#x}")
            print(f"       shutdown={qs[9]:#x} rdb={qs[13]:#x} wrb={qs[14]:#x} num_cip={qs[21]:#x} get_cip={qs[22]:#x}")

print(f"\n确认方法表: {[hex(t) for t in found_tables]}")