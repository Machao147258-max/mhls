# -*- coding: utf-8 -*-
"""libcocos2dlua.so: 精确定位 SSL_METHOD 方法表 (SSLv3/TLSv1/TLSv1_1/TLSv1_2/SSLv23/DTLS)
特征: q0.version = {0x300,0x301,0x302,0x303,0xffff,0xfeff...}
      q4-q8 (accept/connect/read/peek/write) & q21,q22 (num_ciphers/get_cipher) 均指向可执行区
      q23 (ssl3_enc) 指向 DATA 段
SSL_METHOD (1.0.1c): version + 25 指针 = 26 qwords = 208B
"""
import struct

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

EXEC_LO, EXEC_HI = 0x0, 0x10022b8          # LOAD0 RX (offset==vaddr)
EXEC2_LO, EXEC2_HI = 0x15b1000, 0x1906000  # LOAD2 RX (vaddr=offset+0x3d000)
DATA_LO, DATA_HI = 0x1012e08, 0x1580540    # LOAD1 RW (vaddr=offset+0x10000)

def in_exec(v):
    return (EXEC_LO <= v < EXEC_HI) or (EXEC2_LO <= v < EXEC2_HI)
def in_data(v):
    return DATA_LO <= v < DATA_HI

def off2v(o):
    if 0 <= o < 0x10022b8: return o
    if 0x1002e08 <= o < 0x1580540: return o + 0x10000
    if 0x1574000 <= o < 0x1906000: return o + 0x3d000
    return None

VERSIONS = {0x300, 0x301, 0x302, 0x303, 0x2, 0xfb, 0xfd, 0xfeff, 0xfe00, 0xffff}
VNAME = {0x300:'SSLv3', 0x301:'TLSv1', 0x302:'TLSv1.1', 0x303:'TLSv1.2', 0x2:'SSLv2',
         0xffff:'SSLv23', 0xfeff:'DTLSv1', 0xfe00:'DTLS_BAD_VER', 0xfb:'SSLv3.0?', 0xfd:'TLS1?'}

BASE = 0x1002e08
END = 0x1580540
mm = memoryview(d)[BASE:END]
cnt = 0
print("=== SSL_METHOD 表候选 ===")
it = struct.iter_unpack('<Q', mm)
for i, (q0,) in enumerate(it):
        o = BASE + i*8
        v = q0 & 0xFFFFFFFF
        if v not in VERSIONS:
            continue
        if i+26 > len(mm)//8:
            continue
        # 读取 26 个 qword
        qs = struct.unpack_from('<26Q', d, o)
        # q4..q8 exec
        if not (in_exec(qs[4]) and in_exec(qs[5]) and in_exec(qs[6])
                and in_exec(qs[7]) and in_exec(qs[8])):
            continue
        # q21 num_ciphers, q22 get_cipher exec
        if not (in_exec(qs[21]) and in_exec(qs[22])):
            continue
        # q23 ssl3_enc -> data
        if not in_data(qs[23]):
            # 也允许指向 rodata (LOAD0) 里的 enc_data 表
            if not (0x900000 <= qs[23] < EXEC_HI):
                continue
        cnt += 1
        va = off2v(o)
        print(f"  [{va:#010x}] {VNAME.get(v, hex(v)):12s} version={v:#06x}")
        print(f"       new={qs[1]:#x} clear={qs[2]:#x} free={qs[3]:#x}")
        print(f"       accept={qs[4]:#x} connect={qs[5]:#x} read={qs[6]:#x} peek={qs[7]:#x} write={qs[8]:#x}")
        print(f"       shutdown={qs[9]:#x} reneg={qs[10]:#x} reneg_chk={qs[11]:#x}")
        print(f"       get_msg={qs[12]:#x} read_bytes={qs[13]:#x} write_bytes={qs[14]:#x} dispatch={qs[15]:#x}")
        print(f"       ctrl={qs[16]:#x} ctx_ctrl={qs[17]:#x} getcbc={qs[18]:#x} putcbc={qs[19]:#x}")
        print(f"       pending={qs[20]:#x} num_ciphers={qs[21]:#x} get_cipher={qs[22]:#x}")
        print(f"       ssl3_enc={qs[23]:#x} ver_from_cipher={qs[24]:#x} ssl_flush={qs[25]:#x}")
print(f"\n共 {cnt} 个候选")