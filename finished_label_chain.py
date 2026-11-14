# -*- coding: utf-8 -*-
"""确定性破解链:
  'client finished' 字符串 vaddr -> 搜引用者(SSL3_ENC_METHOD 实例栏位[7])
  -> 实例基址 -> 搜引用者(SSL_METHOD 表栏位[23]) -> ssl3_connect/read/write 真实地址
"""
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

# 1) 找 "client finished" / "server finished"
targets = [b'client finished', b'server finished', b'client finished\x00', b'server finished\x00']
for t in targets:
    idx = d.find(t)
    if idx >= 0:
        print(f"串 {t!r} @ fileoff {idx:#x} vaddr {off2v(idx):#x}")
        # 打印附近其他 finished 标签
        for tail in [b'client finished', b'server finished', b'client verify', b'server verify']:
            j = d.find(tail, max(0, idx-64), idx+256)
            if j >= 0:
                print(f"   相邻标签 {tail!r} @ {off2v(j):#x}")

# 2) 扫描数据段 (LOAD1 + LOAD0 rodata) 中引用 finished 串的 qword
print("\n=== 引用 'client finished' 的 qword (SSL3_ENC_METHOD 实例栏位[7] 候选) ===")
fin_v = off2v(d.find(b'client finished'))
refs_to_fin = []
scan_end = 0x1580540
for o in range(0, scan_end, 8):
    q = struct.unpack_from('<Q', d, o)[0]
    if q == fin_v:
        instance = off2v(o) - 7*8   # 栏位[7] 前 7 个 qword 为函数指针
        refs_to_fin.append((off2v(o), instance))
        print(f"  引用 @ {off2v(o):#x} (fileoff {o:#x}) -> 实例基址 {instance:#x}")

# 3) 对每个实例基址, 在数据段搜引用它的 qword (SSL_METHOD 表栏位[23]) 
print("\n=== 引用 enc_data 实例的 qword (SSL_METHOD 表候选) ===")
for _, inst in refs_to_fin:
    for o in range(0, scan_end, 8):
        q = struct.unpack_from('<Q', d, o)[0]
        if q == inst:
            tbl = off2v(o) - 23*8    # 栏位[23]=ssl3_enc
            qs = struct.unpack_from('<26Q', d, v2off(tbl))
            print(f"  {tbl:#x}: version={qs[0]:#x} new={qs[1]:#x} clear={qs[2]:#x} free={qs[3]:#x}")
            print(f"      accept={qs[4]:#x} connect={qs[5]:#x} read={qs[6]:#x} peek={qs[7]:#x} write={qs[8]:#x}")
            print(f"      shutdown={qs[9]:#x} reneg={qs[10]:#x} rn_chk={qs[11]:#x} get_msg={qs[12]:#x}")
            print(f"      rdb={qs[13]:#x} wrb={qs[14]:#x} disp={qs[15]:#x} ctrl={qs[16]:#x} ctx_ctrl={qs[17]:#x}")
            print(f"      getcbc={qs[18]:#x} putcbc={qs[19]:#x} pending={qs[20]:#x} num_cip={qs[21]:#x} get_cip={qs[22]:#x}")
            print(f"      ssl3_enc={qs[23]:#x} vfc={qs[24]:#x} flush={qs[25]:#x}")