# -*- coding: utf-8 -*-
"""Scan Lua 5.1 bytecode blobs: extract source paths + constant-pool strings, keyword match."""
import io, os, sys, struct, tarfile, json

HDR = b'\x1bLuaQ'

def rd(fmt, f):
    sz = struct.calcsize(fmt)
    d = f.read(sz)
    if len(d) < sz:
        raise EOFError('short read')
    return struct.unpack(fmt, d)

def read_string(f):
    n, = rd('<I', f)
    if n == 0:
        return ''
    d = f.read(n)
    return d[:-1].decode('utf-8', 'replace') if d else ''

def read_func(f, depth=0, out=None, maxstr=200000):
    src = read_string(f)
    linedef, lastline = rd('<ii', f)
    nups, numparams, isvarg, maxstack = rd('<BBBB', f)
    out.append(('source', src))
    n, = rd('<i', f)
    f.read(n * 4)  # code
    nk, = rd('<i', f)
    for _ in range(nk):
        t, = rd('<B', f)
        if t == 0:      # nil
            pass
        elif t == 1:    # boolean
            rd('<B', f)
        elif t == 3:    # number
            rd('<d', f)
        elif t == 4:    # string
            s = read_string(f)
            if s and len(out) < maxstr:
                out.append(('str', s))
        else:
            raise ValueError('bad const type %d' % t)
    np, = rd('<i', f)
    for _ in range(np):
        read_func(f, depth + 1, out, maxstr)
    # debug
    n, = rd('<i', f)
    f.read(n * 4)
    n, = rd('<i', f)
    for _ in range(n):
        read_string(f); rd('<ii', f)
    n, = rd('<i', f)
    for _ in range(n):
        read_string(f)
    return out

def parse_bytes(data):
    if not data.startswith(HDR):
        return None
    f = io.BytesIO(data)
    f.read(12)
    out = []
    read_func(f, 0, out)
    return out

def iter_tar(path):
    with tarfile.open(path) as t:
        for m in t:
            if not m.isfile():
                continue
            fh = t.extractfile(m)
            if fh is None:
                continue
            yield m.name, fh.read()

KEYS = ['hp', 'speed', 'damage', 'cool', 'cd', 'attack', 'vision', 'fog', 'camera',
        'visible', 'opacity', 'attribute', 'buff', 'skill', 'cdn', 'hurt', 'heal',
        'collision', 'render', 'culling', 'cocos', 'setVisible']

def main():
    mode = sys.argv[1]
    dst = sys.argv[2]
    kwfile = sys.argv[3] if len(sys.argv) > 3 else None
    kws = [k.lower() for k in (io.open(kwfile, encoding='utf-8').read().split() if kwfile else KEYS)]
    manifest = []
    hit = []
    n = 0
    if mode == 'tar':
        it = iter_tar(dst)
    else:
        def gen():
            for root, _, files in os.walk(dst):
                for fn in files:
                    p = os.path.join(root, fn)
                    yield fn, io.open(p, 'rb').read()
        it = gen()
    for name, data in it:
        n += 1
        try:
            toks = parse_bytes(data)
        except Exception as e:
            manifest.append({'file': name, 'err': str(e)})
            continue
        if toks is None:
            manifest.append({'file': name, 'magic': data[:8].hex()})
            continue
        src = next((v for k, v in toks if k == 'source' and v), '')
        strs = [v for k, v in toks if k == 'str']
        manifest.append({'file': name, 'src': src.lstrip('@'), 'nstr': len(strs)})
        joined = '\n'.join(strs).lower()
        m = [k for k in kws if k in joined]
        if m:
            hit.append({'file': name, 'src': src.lstrip('@'), 'kw': m, 'strs': strs[:400]})
    io.open('scan_manifest.json', 'w', encoding='utf-8').write(json.dumps(manifest, ensure_ascii=False, indent=1))
    io.open('scan_hits.json', 'w', encoding='utf-8').write(json.dumps(hit, ensure_ascii=False, indent=1))
    print('scanned=%d  ok=%d  hits=%d' % (n, sum(1 for x in manifest if 'src' in x), len(hit)))
    for h in hit[:40]:
        print('%-46s %-58s %s' % (h['file'], h['src'][:58], ','.join(h['kw'])))

main()
