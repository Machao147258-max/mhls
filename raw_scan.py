# -*- coding: utf-8 -*-
"""Raw byte-level string harvest from .bin blobs; classify magic; keyword scan."""
import io, os, sys, tarfile, json, re, collections

PRINTABLE = re.compile(rb'[\x20-\x7e]{4,}')

def harvest(data, minlen=4):
    return [m.group().decode('ascii') for m in PRINTABLE.finditer(data) if len(m.group()) >= minlen]

def main():
    tar = sys.argv[1]
    kws = sys.argv[2].split(',') if len(sys.argv) > 2 else []
    magic = collections.Counter()
    index = {}
    hits = []
    n = 0
    with tarfile.open(tar) as t:
        for m in t:
            if not m.isfile():
                continue
            fh = t.extractfile(m)
            data = fh.read()
            n += 1
            magic[data[:6].hex()] += 1
            strs = harvest(data)
            # find lua source marker
            src = ''
            for s in strs[:6]:
                if s.startswith('@') and '.lua' in s:
                    src = s[1:]
                    break
            if not src:
                for s in strs:
                    if '.lua' in s and '/' in s:
                        src = s
                        break
            index[m.name] = src
            if kws:
                low = data.lower()
                found = [k for k in kws if k.lower().encode() in low]
                if found:
                    hits.append({'file': m.name, 'src': src, 'kw': found, 'len': len(data)})
    io.open('raw_index.json', 'w', encoding='utf-8').write(json.dumps(index, ensure_ascii=False, indent=1))
    io.open('raw_hits.json', 'w', encoding='utf-8').write(json.dumps(hits, ensure_ascii=False, indent=1))
    print('files=%d' % n)
    print('--- magic top ---')
    for k, v in magic.most_common(8):
        print('  %s : %d' % (k, v))
    named = sum(1 for v in index.values() if v)
    print('named=%d / %d' % (named, n))
    print('--- kw hits: %d ---' % len(hits))
    for h in hits[:60]:
        print('%-34s %-64s %s' % (h['file'], h['src'][-64:], ','.join(h['kw'])))

main()
