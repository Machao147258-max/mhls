# -*- coding: utf-8 -*-
# 扫描所有已有 dump 找 luac 明文 (1b4c7561 头) — 不需要 key
import os, struct, glob

LUA_HDR = b'\x1bLua'

def scan_file(path, min_size=64, max_size=30*1024*1024):
    """扫描文件中所有疑似 luac (1b4c7561 + 版本 51/53...)"""
    found = []
    try:
        sz = os.path.getsize(path)
        if sz < min_size or sz > 200*1024*1024:
            return found
        with open(path, 'rb') as f:
            data = f.read()
    except Exception:
        return found
    # 找所有 1bLua 头
    pos = 0
    while True:
        i = data.find(LUA_HDR, pos)
        if i < 0:
            break
        # 检查版本: 1b4c756151 (Lua 5.1) 或 1b4c7561xx
        ver = data[i+4:i+6]
        if ver in (b'Q\x00', b'Q\x01', b'\x53\x00') or data[i+4:i+5] in (b'Q', b'5'):
            # 大小判断: 扫描头后 12 字节找 source 长度 (合理 1-200)
            try:
                ln = struct.unpack_from('<I', data, i+12)[0]
                if 0 < ln < 4096:
                    found.append((i, ver))
            except Exception:
                pass
        pos = i + 1
    return found

roots = [
    r'C:\Users\20751\tomdump',
    r'C:\Users\20751\Desktop\猫和老鼠',
]
seen = {}
for root in roots:
    for dirpath, dirnames, filenames in os.walk(root):
        # 跳过已经处理过的目录
        for fn in filenames:
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 200*1024*1024:
                    continue
            except Exception:
                continue
            hits = scan_file(p)
            if hits:
                seen[p] = hits
print('=== 找到含 luac 的文件 ===')
for p, hits in sorted(seen.items()):
    print(f'{p} ({os.path.getsize(p)}B): {len(hits)} 处')
    for off, ver in hits[:5]:
        print(f'    @ {off:#x} ver={ver}')
