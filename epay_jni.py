# -*- coding: utf-8 -*-
"""libepay-crypto.so: 解析 JNINativeMethod 注册表 -> fnPtr 实现函数地址"""
import struct
F = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib\libepay-crypto.so'
d = open(F, 'rb').read()

N = len(d)
# 目标方法名字符串 VA (vaddr==off)
targets = {
    0xa9bea: b'getAesKey',
    0xa9bcc: b'getFlexibleSecret',
    0xa9c13: b'base64Encode',
    0xa9c20: b'base64Decode',
    0xa9c47: b'base64Decode',
}
# 也找一下这些字符串的签名串
# 1) 扫所有 qword 等于目标 VA 的位置 (在非代码段, 可能 .data.rel.ro)
print("== qword 引用目标方法名 VA 的位置 ==")
refs = {}
for va in targets:
    pat = struct.pack('<Q', va)
    pos = 0
    while True:
        i = d.find(pat, pos)
        if i < 0: break
        refs.setdefault(va, []).append(i)
        pos = i + 1
for va, ll in refs.items():
    print("  VA %#x (%s) -> 引用于: %s" % (va, targets[va], ', '.join('%#x' % x for x in ll[:20])))

# 2) 若找到引用, 检查是否构成 JNINativeMethod 数组 (24B 一条: name,sig,fnPtr)
print("\n== JNINativeMethod 候选条目 ==")
for va in targets:
    for ref in refs.get(va, []):
        # name 指针在 [ref-8..ref+16] 附近; 检查 ref 位置是否为 24B 结构起点
        for base in (ref - 16, ref - 8, ref, ref + 8):
            if base < 0 or base + 24 > N: continue
            nm, sg, fn = struct.unpack_from('<QQQ', d, base)
            if nm == va and 0x40000 < fn < 0xb0000:
                # 解析 signature 字符串
                sge = d[sg:].split(b'\x00')[0].decode('latin1', 'replace') if 0 < sg < N else '?'
                print("  base=%#x name=%#x(%s) sig=%#x(%s) fnPtr=%#x" % (base, nm, targets.get(nm, b'?').decode(), sg, sge[:40], fn))
                # 打印该表 24B 周围条目
                for k in range(-2, 5):
                    bb = base + k * 24
                    if bb < 0 or bb + 24 > N: continue
                    nm2, sg2, fn2 = struct.unpack_from('<QQQ', d, bb)
                    if nm2 == 0 and sg2 == 0 and fn2 == 0: print("    [%d] NULL terminator" % k); continue
                    nms = d[nm2:].split(b'\x00')[0].decode('latin1','replace') if 0 < nm2 < N else '?'
                    sgs = d[sg2:].split(b'\x00')[0].decode('latin1','replace') if 0 < sg2 < N else '?'
                    print("    [%d] %#x (%s) sig=%#x (%s) fn=%#x" % (k, nm2, nms, sg2, sgs[:44], fn2))