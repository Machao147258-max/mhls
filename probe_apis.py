# -*- coding: utf-8 -*-
"""probe_apis.py — 深度遍历: 全量拉取 + 路径枚举"""
import urllib.request, ssl, base64, json

ctx = ssl.create_default_context()
UA = 'okhttp/3.12.1'

def get(url, method='GET', data=None, headers=None):
    h = {'User-Agent': UA, 'Accept': '*/*'}
    if headers: h.update(headers)
    body = data.encode() if isinstance(data, str) else data
    req = urllib.request.Request(url, method=method, headers=h, data=body)
    try:
        r = urllib.request.urlopen(req, timeout=25, context=ctx)
        return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, e.read()
    except Exception as e:
        return 'ERR', str(e).encode()

print('=== 1. unisdk 协议模板(全量) ===')
st, b = get('https://protocol.unisdk.netease.com/tpsl/android_class')
print(st, len(b), 'B')
print(b.decode('utf-8', 'replace')[:2000])

print('\n=== 2. unisdk api模板(全量) ===')
st, b = get('https://protocol.unisdk.netease.com/api/template/v89/latest.json')
print(st, len(b), 'B')
print(b.decode('utf-8', 'replace')[:1500])

print('\n=== 3. httpdns / hdserver2 解码 ===')
for name, url in [('mbdl', 'https://mbdl.update.netease.com/httpdns.mbdl'),
                  ('hdserver2', 'https://dns.update.netease.com/hdserver2')]:
    st, b = get(url)
    try:
        print(name, '→', base64.b64decode(b).decode('utf-8', 'replace')[:300])
    except Exception:
        print(name, '→', b[:200])

print('\n=== 4. nglbs 带 gameid ===')
for url in ['https://nglbs.nie.netease.com?gameid=h18',
            'https://nglbs.nie.netease.com/?gameid=h18',
            'https://nglbs.nie.netease.com/v1?gameid=h18']:
    st, b = get(url)
    print(url.split('//')[1][:40], st, b[:120])

print('\n=== 5. 易盾 preCheck 带参数 ===')
st, b = get('https://ye.dun.163yun.com/v1/preCheck', 'POST', 'data={"gameId":"h18"}', {'Content-Type': 'application/json'})
print(st, b[:200])

print('\n=== 6. unisdk 其他路径 ===')
for p in ['/tpsl/', '/tpsl/android', '/tpsl/android_global', '/api/template/v89/', '/api/template/', '/api/', '/tpsl/android_class?format=json']:
    st, b = get('https://protocol.unisdk.netease.com' + p)
    print(p, '→', st, b[:100])

print('\n=== 7. whoami 带参数尝试 ===')
for u in ['https://whoami.nie.easebar.com/v7?product=h18',
          'https://whoami.nie.easebar.com/v7?product=h18&token=1',
          'https://whoami.nie.easebar.com/v2']:
    st, b = get(u)
    print(u.split('//')[1][:45], st, b[:100])