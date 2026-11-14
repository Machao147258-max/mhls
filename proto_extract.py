# -*- coding: utf-8 -*-
"""
proto_extract.py — 从内存 dump 解析 Lua 5.1 Proto 对象,重建 .luac
流程: 干净名字 TString → 找指向它的 8B 指针(source 字段) → 反推 Proto 起点
       → 校验 size 字段 → 读 code/常量/子Proto → 序列化成标准 luac
用法: python proto_extract.py
"""
import os, re, struct, glob, json, bisect

BASE = r'C:\Users\20751\tomdump\dd_live_1973'
OUT = os.path.join(BASE, 'protos')
os.makedirs(OUT, exist_ok=True)

# 1. 载入段
segs = []          # (start, end, data)
for f in sorted(glob.glob(os.path.join(BASE, 's*.bin'))):
    idx = int(os.path.basename(f)[1:-4])
    d = open(f, 'rb').read()
    segs.append((idx, d))
segmap = json.load(open(os.path.join(BASE, 'segmap.json')))
starts = [s[0] for s in segmap]
ends = [s[1] for s in segmap]
datas = [segs[i][1] for i in range(len(segmap))]

def read_va(va, n):
    """读任意 VA 的 n 字节; 返回 bytes 或 None"""
    i = bisect.bisect_right(starts, va) - 1
    if i < 0 or va + n > ends[i]:
        return None
    off = va - starts[i]
    return datas[i][off:off + n]

def u32(b, o): return struct.unpack_from('<I', b, o)[0]
def u64(b, o): return struct.unpack_from('<Q', b, o)[0]

def tstring_str(va):
    """读 TString 内容"""
    hdr = read_va(va, 32)
    if hdr is None:
        return None
    # CommonHeader 16B, hash 8B, len 8B, data...
    ln = u64(hdr, 24)
    if ln <= 0 or ln > 2000:
        return None
    d = read_va(va + 32, ln)
    if d is None:
        return None
    return d.rstrip(b'\x00').decode('latin-1', 'replace')

def parse_proto(proto_va, depth=0, visited=None):
    """从 Proto 起点递归提取,返回 luac 序列化字节 或 None"""
    if visited is None:
        visited = set()
    if proto_va in visited or depth > 64:
        return None
    visited.add(proto_va)
    hdr = read_va(proto_va, 116)
    if hdr is None:
        return None
    k_ptr = u64(hdr, 16)
    code_ptr = u64(hdr, 24)
    p_ptr = u64(hdr, 32)
    src_ptr = u64(hdr, 64)
    sizeupv = u32(hdr, 72); sizek = u32(hdr, 76)
    sizecode = u32(hdr, 80); sizelineinfo = u32(hdr, 84)
    sizep = u32(hdr, 88); sizelocvars = u32(hdr, 92)
    linedefined = u32(hdr, 96); lastlinedefined = u32(hdr, 100)
    nups = hdr[112]; params = hdr[113]; vararg = hdr[114]; maxstack = hdr[115]
    # 校验
    if not (0 <= sizecode <= 2000000 and 0 <= sizek <= 200000 and 0 <= sizep <= 20000
            and 0 <= nups <= 200 and 0 <= maxstack <= 250 and linedefined <= 10000000):
        return None
    src = tstring_str(src_ptr) if src_ptr else None
    # code
    cb = read_va(code_ptr, sizecode * 4)
    if cb is None:
        return None
    # 常量: TValue = value(8) + tt(1) + pad(7)
    kvals = []
    for i in range(sizek):
        tv = read_va(k_ptr + i * 16, 16)
        if tv is None:
            return None
        tt = tv[8]
        val = u64(tv, 0)
        if tt == 3:      # number double
            dbl = struct.unpack('<d', tv[:8])[0]
            kvals.append(('num', dbl))
        elif tt == 4:    # string
            s = tstring_str(val)
            kvals.append(('str', s if s is not None else '?'))
        elif tt == 1:
            kvals.append(('bool', bool(val)))
        elif tt == 0:
            kvals.append(('nil', None))
        else:
            kvals.append(('userdata', None))
    # 子 proto
    protos = []
    for i in range(sizep):
        pv = u64(read_va(p_ptr + i * 8, 8) or b'\x00' * 8, 0)
        sub = parse_proto(pv, depth + 1, visited)
        if sub is None:
            return None
        protos.append(sub)
    return (src, linedefined, lastlinedefined, nups, params, vararg, maxstack,
            cb, kvals, protos)

# ---- luac 序列化 ----
def ser_str(s):
    if s is None:
        return struct.pack('<I', 0)
    b = s.encode('utf-8') + b'\x00'
    return struct.pack('<I', len(b)) + b

def ser_proto(p):
    src, ld, lld, nups, params, vararg, maxstack, code, kvals, protos = p
    out = bytearray()
    out += ser_str(src)
    out += struct.pack('<ii', ld, lld)
    out += bytes([nups, params, vararg, maxstack])
    out += struct.pack('<I', len(code) // 4) + code
    out += struct.pack('<I', len(kvals))
    for kind, v in kvals:
        if kind == 'num':
            out += b'\x03' + struct.pack('<d', v)
        elif kind == 'str':
            out += b'\x04' + ser_str(v)
        elif kind == 'bool':
            out += b'\x01' + (b'\x01' if v else b'\x00')
        else:
            out += b'\x00'
    out += struct.pack('<I', 0)   # lineinfo
    out += struct.pack('<I', 0)   # locvars
    out += struct.pack('<I', 0)   # upvalue names
    out += struct.pack('<I', len(protos))
    for sub in protos:
        out += ser_proto(sub)
    return bytes(out)

def make_luac(top):
    return b'\x1bLua\x51\x00\x01\x04\x04\x04\x08\x00' + ser_proto(top)

# ---- 主流程 ----
# 收集干净名字 TString
name_vas = {}     # name -> va
for i, (st, en) in enumerate(zip(starts, ends)):
    d = datas[i]
    for m in re.finditer(rb'@src/[a-zA-Z0-9_/\.\-]{5,80}\.lua\x00', d):
        name = m.group()[:-1].decode()
        va = st + m.start()
        name_vas.setdefault(name, va)

print(f'干净脚本名: {len(name_vas)}', flush=True)

# 找 source 指针并解析
found = 0
results = {}
items = list(name_vas.items())
for ni, (name, tva) in enumerate(items):
    if found > 400:
        break
    if ni % 40 == 0:
        print(f'-- 进度 {ni}/{len(items)}, 已重建 {found}', flush=True)
    p = struct.pack('<Q', tva)
    for i, (st, en) in enumerate(zip(starts, ends)):
        d = datas[i]
        j = 0
        while True:
            j = d.find(p, j)
            if j < 0:
                break
            ptr_va = st + j
            proto_start = ptr_va - 64
            if proto_start < st:
                j += 1
                continue
            try:
                top = parse_proto(proto_start)
            except Exception:
                top = None
            if top:
                src = top[0]
                luac = make_luac(top)
                if len(luac) > 100:
                    fn = os.path.join(OUT, re.sub(r'[^\w.]', '_', (src or 'x')) + '.luac')
                    with open(fn, 'wb') as f:
                        f.write(luac)
                    found += 1
                    results[name] = len(luac)
                    print(f'[{found}] {name} ({len(luac)}B)', flush=True)
                    break
            j += 1

print(f'\n共重建 {found} 个 luac → {OUT}')