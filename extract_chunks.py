# -*- coding: utf-8 -*-
# 从内存 dump 段提取 Lua 5.1 字节码 chunk(严格按二进制格式递归解析长度)
# 用法: python extract_chunks.py dump*.bin -o <outdir>
import sys, os, struct

def u32(b, o): return struct.unpack_from('<I', b, o)[0]

def parse_function(b, p, trace=None):
    """解析一个 Function proto(从 p 起),返回结束偏移。trace 非空时记录偏移。"""
    def read_str():
        nonlocal p
        if p + 4 > len(b):
            raise ValueError('trunc')
        l = u32(b, p); p += 4
        if l > 64 * 1024 * 1024:
            raise ValueError('str %d' % l)
        s = b[p:p + max(l - 1, 0)].decode('latin-1', 'replace') if 0 < l < 4096 else ''
        if l > len(b) - p:
            raise ValueError('str overflow')
        p += l
        return s

    if p + 4 > len(b):
        raise ValueError('trunc')
    s_len = u32(b, p); p += 4
    name = ''
    if 0 < s_len < 4096:
        name = b[p:p + max(s_len - 1, 0)].decode('latin-1', 'replace')
    if s_len > len(b) - p:
        raise ValueError('src overflow')
    p += s_len
    p += 4 + 4                       # linedefined, lastlinedefined
    p += 1 + 1 + 1 + 1               # nups, params, isvararg, maxstack
    n = u32(b, p); p += 4            # code[]
    if n > 8 * 1024 * 1024: raise ValueError('code %d' % n)
    if n * 4 > len(b) - p: raise ValueError('code ovf')
    p += n * 4
    n = u32(b, p); p += 4            # constants[]
    if n > 4 * 1024 * 1024: raise ValueError('const %d' % n)
    for _ in range(n):
        if p >= len(b): raise ValueError('const trunc')
        t = b[p]; p += 1
        if t == 0: pass
        elif t == 1: p += 1
        elif t == 3: p += 8
        elif t == 4: read_str()
        else: raise ValueError('const type %d' % t)
    # ---- Lua 5.1 debug 段: lineinfo, locvars, upvalue names (strip 时计数为 0) ----
    n = u32(b, p); p += 4            # lineinfo[] (char each)
    if n > (1 << 24): raise ValueError('lineinfo %d' % n)
    p += n
    n = u32(b, p); p += 4            # locvars[]
    if n > (1 << 20): raise ValueError('locvars %d' % n)
    for _ in range(n):
        read_str()
        p += 4 + 4                   # startpc, endpc
    n = u32(b, p); p += 4            # upvalue names[]
    if n > (1 << 20): raise ValueError('upvnames %d' % n)
    for _ in range(n):
        read_str()
    n = u32(b, p); p += 4            # protos[]
    if n > (1 << 20): raise ValueError('proto %d' % n)
    for _ in range(n):
        p = parse_function(b, p)
    if trace is not None:
        trace.append('%#x src=%r proto=%d' % (name, n))
    return p

def scan_chunks(b, dbg=False):
    """扫描全部 1b 4c 75 61 51 开头且可完整解析的 chunk,返回 [(name, off, end)]"""
    out = []
    i = 0
    while True:
        j = b.find(b'\x1bLua\x51', i)
        if j < 0: break
        # 校验头参数: 51 00 01 04 04 04 08 00
        if j + 12 <= len(b) and b[j + 5:j + 12] == b'\x00\x01\x04\x04\x04\x08\x00':
            try:
                end = parse_function(b, j + 12)
            except Exception:
                i = j + 1
                continue
            name = 'chunk'
            try:
                s_len = u32(b, j + 12)
                s = b[j + 16:j + 16 + s_len - 1]
                stop = s.find(b'\x00')
                if stop >= 0:
                    s = s[:stop]
                if s:
                    name = s.decode('latin-1', 'replace')
            except Exception:
                pass
            out.append((name, j, end))
            i = end
            continue
        i = j + 1
    return out

def main():
    import glob
    argv = sys.argv[1:]
    args = []
    i = 0
    while i < len(argv):
        if argv[i] == '-o':
            i += 2
            continue
        args += glob.glob(argv[i]) or [argv[i]]
        i += 1
    outdir = None
    if '-o' in sys.argv:
        outdir = sys.argv[sys.argv.index('-o') + 1]
    if not outdir:
        outdir = 'chunks_out'
    os.makedirs(outdir, exist_ok=True)
    total = 0
    for fn in args:
        data = open(fn, 'rb').read()
        chunks = scan_chunks(data)
        if not chunks:
            print(f'{os.path.basename(fn)}: 无 chunk')
            continue
        print(f'{os.path.basename(fn)}: {len(chunks)} chunks')
        for name, off, end in chunks:
            safe = (name or 'nameless').replace('/', '__').replace('@', '').replace('\\', '__')
            safe = ''.join(c for c in safe if c.isalnum() or c in '._-')[:80]
            fname = f'{outdir}/{len(os.listdir(outdir)):04d}_{safe}.luac'
            with open(fname, 'wb') as f:
                f.write(data[off:end])
            total += 1
            print(f'    {name or "(无名字)"}  @0x{off:x} size={end-off}')
    print(f'共提取 {total} 个')

if __name__ == '__main__':
    main()