# -*- coding: utf-8 -*-
"""cdn_pull.py — 从 CDN 全量拉取资源(按 filelist patch_version 路由)
用法: python cdn_pull.py <src|all> [并发数]
"""
import json, os, sys, hashlib, threading, queue, urllib.request, ssl, time

FL = r'C:\Users\20751\tomdump\device_runtime\filelist_high.json'
OUT = r'C:\Users\20751\tomdump\cdn_pull'
MODE = sys.argv[1] if len(sys.argv) > 1 else 'src'
CONC = int(sys.argv[2]) if len(sys.argv) > 2 else 16
ctx = ssl.create_default_context()
UA = 'okhttp/3.12.1'

fl = json.load(open(FL))
items = []
for f in fl['files']:
    if MODE == 'src' and not f['file'].startswith('package/src'):
        continue
    items.append(f)

def dst_path(f):
    return os.path.join(OUT, f['file'])

ok = miss = bad = 0
fail = []

def worker():
    global ok, miss, bad
    while True:
        try:
            f = q.get_nowait()
        except queue.Empty:
            return
        try:
            dp = dst_path(f)
            if os.path.exists(dp) and os.path.getsize(dp) == f['size']:
                if hashlib.md5(open(dp, 'rb').read()).hexdigest() == f['md5']:
                    ok += 1
                    q.task_done()
                    continue
            u = f'https://h18.gph.netease.com/patch.{f["patch_version"]}.publish/resource/{f["file"]}'
            for attempt in range(3):
                try:
                    req = urllib.request.Request(u, headers={'User-Agent': UA})
                    r = urllib.request.urlopen(req, timeout=30, context=ctx)
                    b = r.read()
                    if hashlib.md5(b).hexdigest() != f['md5']:
                        raise ValueError('md5 mismatch')
                    os.makedirs(os.path.dirname(dp), exist_ok=True)
                    open(dp, 'wb').write(b)
                    ok += 1
                    break
                except Exception as e:
                    if attempt == 2:
                        raise
                    time.sleep(1)
        except Exception as e:
            bad += 1
            fail.append((f['file'], str(e)[:60]))
        q.task_done()

q = queue.Queue()
for f in items:
    q.put(f)
ts = time.time()
threads = [threading.Thread(target=worker) for _ in range(CONC)]
for t in threads: t.start()
for t in threads: t.join()
print(f'完成: {ok} 成功 / {bad} 失败 / 共 {len(items)}  耗时 {time.time()-ts:.0f}s')
for ff in fail[:10]:
    print('  失败:', ff)