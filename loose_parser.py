# -*- coding: utf-8 -*-
"""容忍截断的 loose 解析器: 从(可能截断的)luac 缓冲提取 code/consts(字符串常量)/protos 数量
对 protoc.lua 等尾部 debug 信息被截断的脚本有效(主体在 consts)
"""
import struct, json, os, sys

def parse_loose(b, pos=12, depth=0, state=None):
    """返回 (end_pos, proto_dict) 或 None; 对 debug 段越界宽容"""
    if state is None:
        state = {"truncated": False}
    try:
        if pos + 4 > len(b): return None
        src_len = struct.unpack_from('<I', b, pos)[0]
        if src_len > 0x100000: return None
        pos += 4 + src_len
        pos += 12  # linedefined + lastlinedefined + nups/numparams/isvararg/maxstack
        if pos + 4 > len(b): return None
        sc = struct.unpack_from('<I', b, pos)[0]
        if sc > 0x1000000: return None
        pos += 4
        n_avail = (len(b) - pos) // 4
        code = list(struct.unpack_from('<%dI' % min(sc, n_avail), b, pos)) if min(sc, n_avail) > 0 else []
        if sc > n_avail:
            state["truncated"] = True
        pos += sc * 4
        consts = []
        if pos + 4 > len(b): return None
        sizek = struct.unpack_from('<I', b, pos)[0]
        pos += 4
        for _ in range(sizek):
            if pos >= len(b):
                state["truncated"] = True
                break
            t = b[pos]; pos += 1
            if t == 0:
                consts.append(None)
            elif t == 1:
                if pos >= len(b): state["truncated"] = True; break
                consts.append(bool(b[pos])); pos += 1
            elif t == 3:
                if pos + 8 > len(b): state["truncated"] = True; break
                consts.append(struct.unpack_from('<d', b, pos)[0]); pos += 8
            elif t == 4:
                if pos + 4 > len(b): state["truncated"] = True; break
                l = struct.unpack_from('<I', b, pos)[0]
                if l > 0x100000: return None
                pos += 4
                s = b[pos:pos+l].decode('utf-8', 'replace')
                consts.append(s)
                pos += l
                if pos > len(b): state["truncated"] = True; break
            else:
                return None
        if pos + 4 > len(b):
            state["truncated"] = True
            return pos, {'code': code, 'consts': consts, 'protos': []}
        sizep = struct.unpack_from('<I', b, pos)[0]
        pos += 4
        protos = []
        for _ in range(sizep):
            if pos + 4 > len(b):
                state["truncated"] = True
                break
            r = parse_loose(b, pos, depth + 1, state)
            if r is None:
                state["truncated"] = True
                break
            ep, p = r
            protos.append(p)
            pos = ep
        # debug 段(lineinfo/locvars/upvalues) - 宽容跳过
        for field in range(3):
            if pos + 4 > len(b):
                state["truncated"] = True
                break
            n = struct.unpack_from('<I', b, pos)[0]
            if n > 0x1000000: break
            pos += 4
            if field == 0:
                pos += n * 4
            elif field == 1:
                ok = True
                for _ in range(n):
                    if pos + 4 > len(b): ok = False; break
                    l2 = struct.unpack_from('<I', b, pos)[0]
                    if l2 > 0x100000: ok = False; break
                    pos += 4 + l2 + 8
                if not ok:
                    state["truncated"] = True
                    break
            else:
                ok = True
                for _ in range(n):
                    if pos + 4 > len(b): ok = False; break
                    l2 = struct.unpack_from('<I', b, pos)[0]
                    pos += 4 + l2
                if not ok:
                    state["truncated"] = True
                    break
        return pos, {'code': code, 'consts': consts, 'protos': protos}
    except Exception:
        return None

def all_string_consts(p, acc=None):
    if acc is None:
        acc = []
    for c in p['consts']:
        if isinstance(c, str):
            acc.append(c)
    for sp in p['protos']:
        all_string_consts(sp, acc)
    return acc

if __name__ == '__main__':
    # 对 protoc.lua 提取全部字符串
    import glob
    best = None
    for pat in [r"C:\Users\20751\Desktop\猫和老鼠\PLAINS\batch1\L_1061_1536.bin",
                r"C:\Users\20751\Desktop\猫和老鼠\PLAINS\ls\L_1061_1536.bin"]:
        if os.path.exists(pat):
            best = pat
            break
    if not best:
        print("no file"); sys.exit(1)
    b = open(best, 'rb').read()
    st = {"truncated": False}
    r = parse_loose(b, state=st)
    print("header ok:", b[:4], "truncated:", st["truncated"], "proto:", r is not None)
    if r:
        ep, p = r
        strs = all_string_consts(p)
        print("total string consts:", len(strs))
        out = r"C:\Users\20751\Desktop\猫和老鼠\REV_ALL2\protoc_consts.txt"
        open(out, "w", encoding="utf-8").write("\n".join(strs))
        print("written:", out)
        # 打印前 80 条
        for s in strs[:80]:
            print(" ", s)