# -*- coding: utf-8 -*-
"""全文件范围扫描 SSL_METHOD 方法表 (含 LOAD0 只读段 offset==vaddr)
特征: q0.version(低32)∈{0x300,0x301,0x302,0x303,0xffff,0xfeff}
      q4..q8(accept/connect/read/peek/write) 与 q21,q22 全部 EXEC
"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()
SZ = len(d)

def off_is_exec(o):
    return (0 <= o < 0x10022b8) or (0x1574000 <= o < 0x1906000)
def off_is_data(o):
    return 0x1002e08 <= o < 0x1580540
def off2v(o):
    if 0 <= o < 0x10022b8: return o
    if 0x1002e08 <= o < 0x1580540: return o + 0x10000
    if 0x1574000 <= o < 0x1906000: return o + 0x3d000
    return None

VERSIONS = {0x300, 0x301, 0x302, 0x303, 0xffff, 0xfeff, 0xfb, 0xfd, 0xfe00}
VNAME = {0x300:'SSLv3', 0x301:'TLSv1', 0x302:'TLSv1.1', 0x303:'TLSv1.2', 0xffff:'SSLv23',
         0xfeff:'DTLSv1', 0xfe00:'DTLS_BAD', 0xfb:'?', 0xfd:'?'}

def v_ok(o):
    if o + 26*8 > SZ: return None
    q = struct.unpack_from('<Q', d, o)[0]
    return (q & 0xFFFFFFFF) in VERSIONS

def check_table(o):
    qs = struct.unpack_from('<26Q', d, o)
    ver = qs[0] & 0xFFFFFFFF
    # q4 q5 q6 q7 q8 全 EXEC
    for slot in (4, 5, 6, 7, 8, 21, 22):
        v = qs[slot]
        # vaddr 转换: 是否在 EXEC 区间
        if not ((0 <= v < 0x10022b8) or (0x15b1000 <= v < 0x1906000)):
            return None
    return qs

found = []
# 扫全文件 8 对齐
for o in range(0, SZ - 26*8, 8):
    r = v_ok(o)
    if not r:
        continue
    qs = check_table(o)
    if qs:
        found.append((o, qs))

print(f"== {len(found)} 个方法表候选 ==\n")
for o, qs in found:
    va = off2v(o)
    ver = qs[0] & 0xFFFFFFFF
    print(f"[{va:#x}] {VNAME.get(ver, hex(ver))} version={ver:#x}")
    print(f"    new={qs[1]:#x} clear={qs[2]:#x} free={qs[3]:#x}")
    print(f"    accept={qs[4]:#x} connect={qs[5]:#x} read={qs[6]:#x} peek={qs[7]:#x} write={qs[8]:#x}")
    print(f"    shutdown={qs[9]:#x} reneg={qs[10]:#x} rn_chk={qs[11]:#x} get_msg={qs[12]:#x}")
    print(f"    rdb={qs[13]:#x} wrb={qs[14]:#x} disp={qs[15]:#x} ctrl={qs[16]:#x} ctx_ctrl={qs[17]:#x}")
    print(f"    getcbc={qs[18]:#x} putcbc={qs[19]:#x} pending={qs[20]:#x} num_cip={qs[21]:#x} get_cip={qs[22]:#x}")
    print(f"    ssl3_enc={qs[23]:#x} vfc={qs[24]:#x} flush={qs[25]:#x}\n")