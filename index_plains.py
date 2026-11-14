# -*- coding: utf-8 -*-
"""批量扫描 PLAINS 目录所有 luac 缓冲, 提取源码路径/主函数大小/结构有效性"""
import struct, os, sys, json, glob

ROOT = r"C:\Users\20751\Desktop\猫和老鼠\PLAINS"

def parse_proto_head(b, pos=12):
    """尽量解析 proto 头, 提取 source 字符串; 失败返回 None"""
    try:
        src_len = struct.unpack_from('<I', b, pos)[0]
        if src_len > 0x100000 or pos + 4 + src_len > len(b):
            return None
        src = b[pos+4:pos+4+src_len]
        pos += 4 + src_len
        pos += 12
        sc = struct.unpack_from('<I', b, pos)[0]
        if sc > 0x1000000:
            return None
        return src, sc
    except Exception:
        return None

def main():
    results = []
    for p in glob.glob(os.path.join(ROOT, "**", "*.bin"), recursive=True):
            try:
                data = open(p, 'rb').read()
            except Exception:
                continue
            if len(data) < 28 or data[:4] != b'\x1bLua':
                continue
            h = parse_proto_head(data)
            if h is None:
                results.append((os.path.relpath(p, ROOT), len(data), 'BROKEN', ''))
                continue
            src, sc = h
            # 路径字符串: 去掉开头的 @
            s = src.decode('utf-8', 'replace')
            results.append((os.path.relpath(p, ROOT), len(data), 'OK', s))
    # 输出到文件(避免控制台编码问题)
    out = os.path.join(ROOT, '_src_index.json')
    json.dump(results, open(out, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    ok = sum(1 for r in results if r[2] == 'OK')
    print(f"total={len(results)} ok={ok} broken={len(results)-ok} -> {out}")

if __name__ == '__main__':
    main()