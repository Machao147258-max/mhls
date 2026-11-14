# -*- coding: utf-8 -*-
# 极简 dex 字符串表解析器: 读全部字符串常量
# 用法: python dex_strings.py <file.dex> [过滤词...]
import sys, struct

def mutf8(data, off):
    out = []
    i = off
    while True:
        b = data[i]; i += 1
        if b == 0:
            break
        if b < 0x80:
            out.append(chr(b))
        elif (b & 0xE0) == 0xC0:
            out.append(chr(((b & 0x1F) << 6) | (data[i] & 0x3F))); i += 1
        elif (b & 0xF0) == 0xE0:
            out.append(chr(((b & 0x0F) << 12) | ((data[i] & 0x3F) << 6) | (data[i+1] & 0x3F))); i += 2
        else:
            # 3字节代理对
            u = ((b & 0x07) << 18) | ((data[i] & 0x3F) << 12) | ((data[i+1] & 0x3F) << 6) | (data[i+2] & 0x3F)
            u -= 0x10000
            out.append(chr(0xD800 + (u >> 10))); out.append(chr(0xDC00 + (u & 0x3FF)))
            i += 3
    return ''.join(out)

def strings_of(fn):
    d = open(fn, 'rb').read()
    string_ids_size, string_ids_off = struct.unpack_from('<II', d, 0x38 + 8)
    out = []
    for i in range(string_ids_size):
        s_off = struct.unpack_from('<I', d, string_ids_off + i * 4)[0]
        try:
            s = mutf8(d, s_off)
            out.append(s)
        except Exception:
            out.append('?')
    return out

if __name__ == '__main__':
    fn = sys.argv[1]
    filters = sys.argv[2:]
    ss = strings_of(fn)
    print(f'{fn}: {len(ss)} 个字符串')
    if filters:
        for s in ss:
            if any(f.lower() in s.lower() for f in filters):
                print(' ', repr(s)[:160])
    else:
        for s in ss[:50]:
            print(' ', repr(s)[:160])