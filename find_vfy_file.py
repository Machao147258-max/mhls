# -*- coding: utf-8 -*-
"""搜源文件名字符串 (x509_vfy.c / s3_clnt.c / s3_srvr.c / t1_clnt.c 等) 并找引用者"""
import struct, re
from capstone import *

F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libcocos2dlua.so'
d = open(F, 'rb').read()

TARGETS = [b'x509_vfy.c', b's3_clnt.c', b's3_srvr.c', b't1_clnt.c', b'ssl_lib.c', b'x509_lu.c', b't1_lib.c']
print("=== 源文件名字符串位置 ===")
for t in TARGETS:
    idxs = [m.start() for m in re.finditer(re.escape(t), d)]
    print(f"  {t.decode():12s}: {[hex(i) for i in idxs]}")

# 重点: x509_vfy.c 与 s3_clnt.c 的引用
def find_adrp_ldr_refs(str_va):
    """扫描代码段: adrp xN,#page; ldr/add xN,[xN,#off] 加载 str_va 的指令对,
    返回引用指令地址。步进扫描全文件。"""
    refs = []
    # 转文件偏移
    so = str_va
    # 扫描 adrp (0x90000000 | ...) 后跟 ldr/add
    REGIONS = [(0x0, 0x10022b8), (0x1574000, len(d))]
    for lo, hi in REGIONS:
        cur = lo
        while cur < hi - 8:
            w1 = struct.unpack_from('<I', d, cur)[0]
            if (w1 & 0x9F000000) == 0x90000000:
                rd1 = w1 & 0x1F
                imm1 = ((w1 >> 5) & 0x7FFFF) << 12
                page = (cur & ~0xFFF) + imm1
                if page == (str_va & ~0xFFF):
                    w2 = struct.unpack_from('<I', d, cur+4)[0]
                    rd2 = w2 & 0x1F
                    if rd1 == rd2:
                        if (w2 & 0xFFC00000) == 0xF9400000:  # ldr
                            off = (w2 >> 10) & 0xFFF
                            if (page + off) == str_va:
                                refs.append(cur)
                        elif (w2 & 0xFF800000) == 0x91000000:  # add imm
                            off = (w2 >> 10) & 0xFFF
                            if (page + off) == str_va:
                                refs.append(cur)
            cur += 4
    return refs

def find_str_addr(s):
    i = d.find(s)
    return i

print("\n=== x509_vfy.c 引用者 (内含 ERR_put_error 的函数 = vfy.c 函数) ===")
sv = find_str_addr(b'x509_vfy.c\0')
print(f"  'x509_vfy.c' @ {sv:#x}")
refs = find_adrp_ldr_refs(sv)
print(f"  引用指令: {[hex(r) for r in refs]}")

print("\n=== s3_clnt.c 引用者 ===")
sv2 = find_str_addr(b's3_clnt.c\0')
print(f"  's3_clnt.c' @ {sv2:#x}")
refs2 = find_adrp_ldr_refs(sv2)
print(f"  引用指令: {[hex(r) for r in refs2]}")