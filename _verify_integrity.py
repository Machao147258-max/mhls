# -*- coding: utf-8 -*-
"""
_verify_integrity.py —— 猫和老鼠 目录自校验器（放在目录根部，随目录一起走）

用法:
    python _verify_integrity.py            # 全量校验（6.16GB，约 1 分钟）
    python _verify_integrity.py --quick    # 只校验文件数/大小，不重算哈希

说明:
    _MANIFEST_SHA256.txt 记录 11300 个数据文件的 SHA256 + 字节数。
    本脚本与清单文件本身不在清单内（自引用问题）。
    退出码 0 = 完整；1 = 有缺失/大小/hash 不符。
"""
import hashlib
import io
import os
import re
import sys
import time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = os.path.dirname(os.path.abspath(__file__))
MAN = os.path.join(ROOT, '_MANIFEST_SHA256.txt')
SELF = {'_MANIFEST_SHA256.txt', '_verify_integrity.py'}
RX = re.compile(r'^([0-9a-f]{64})\s+(\d+)\s\s(.*)$')


def sha256(path, bs=1 << 20):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            b = f.read(bs)
            if not b:
                break
            h.update(b)
    return h.hexdigest()


def main():
    quick = '--quick' in sys.argv
    if not os.path.exists(MAN):
        print('[FAIL] 清单缺失:', MAN)
        return 1
    rows = []
    head = ''
    for line in open(MAN, encoding='utf-8'):
        line = line.rstrip('\n')
        if not line:
            continue
        if line.startswith('#'):
            head = line
            continue
        m = RX.match(line)
        if m:
            rows.append((m.group(1), int(m.group(2)), m.group(3)))
    print(head)
    print('清单条目 %d  声明字节 %d (%.2f GB)' % (len(rows), sum(r[1] for r in rows),
                                              sum(r[1] for r in rows) / 1024 ** 3))

    cur = {}
    for r, ds, fs in os.walk(ROOT):
        for f in fs:
            if f in SELF:
                continue
            p = os.path.join(r, f)
            cur[os.path.relpath(p, ROOT)] = os.path.getsize(p)

    miss = [n for _, _, n in rows if n not in cur]
    extra = [n for n in cur if n not in {r[2] for r in rows}]
    size_bad = [(n, cur[n], s) for _, s, n in rows if n in cur and cur[n] != s]
    print('磁盘文件 %d  清单缺失 %d  清单外新增 %d  大小不符 %d'
          % (len(cur), len(miss), len(extra), len(size_bad)))
    for n in miss[:10]:
        print('  MISSING', n)
    for n in extra[:10]:
        print('  EXTRA  ', n)
    for n, a, b in size_bad[:10]:
        print('  SIZE   ', n, a, '!=', b)

    hash_bad = []
    if not quick:
        t0 = time.time()
        for i, (h, s, n) in enumerate(rows, 1):
            if n in miss:
                continue
            if sha256(os.path.join(ROOT, n)) != h:
                hash_bad.append(n)
            if i % 3000 == 0:
                print('  校验 %5d/%d  %.0fs' % (i, len(rows), time.time() - t0))
        print('哈希不符 %d 条，耗时 %.1fs' % (len(hash_bad), time.time() - t0))
        for n in hash_bad[:10]:
            print('  HASH   ', n)

    ok = not (miss or extra or size_bad or hash_bad)
    print('\n结论:', 'PASS 目录完整' if ok else 'FAIL 存在差异')
    return 0 if ok else 1


if __name__ == '__main__':
    sys.exit(main())
