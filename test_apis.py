# -*- coding: utf-8 -*-
"""test_apis.py — 批量探测网易系 API 端点(宿主机侧, 零风险)"""
import urllib.request, ssl, json, sys

UA = 'okhttp/3.12.1'
ENDPOINTS = [
    ('unisdk 协议模板', 'https://protocol.unisdk.netease.com/tpsl/android_class', 'GET'),
    ('unisdk api模板', 'https://protocol.unisdk.netease.com/api/template/v89/latest.json', 'GET'),
    ('appdump config', 'https://appdump.nie.netease.com/config', 'GET'),
    ('appdump device', 'https://appdump.nie.netease.com/device', 'GET'),
    ('httpdns mbdl', 'https://mbdl.update.netease.com/httpdns.mbdl', 'GET'),
    ('hdserver2', 'https://dns.update.netease.com/hdserver2', 'GET'),
    ('whoami v7', 'https://whoami.nie.easebar.com/v7', 'GET'),
    ('whoami-ipv4', 'https://whoami-ipv4.nie.easebar.com/v7', 'GET'),
    ('易盾 preCheck', 'https://ye.dun.163yun.com/v1/preCheck', 'GET'),
    ('nglbs', 'https://nglbs.nie.netease.com', 'GET'),
    ('grs feature2', 'https://g0.gsf.easebar.com/feature2/', 'GET'),
    ('grs feature query', 'https://g0.gsf.easebar.com/feature/query.json', 'GET'),
    ('unisec 上报', 'https://unisec-inner.nie.netease.com', 'GET'),
    ('data-detect', 'https://data-detect.nie.easebar.com/client/mobile_upload', 'POST'),
    ('matrix clientlog', 'https://applog.matrix.netease.com/client/sdk/clientlog', 'GET'),
]

ctx = ssl.create_default_context()
for name, url, method in ENDPOINTS:
    try:
        req = urllib.request.Request(url, method=method, headers={'User-Agent': UA, 'Accept': '*/*'})
        r = urllib.request.urlopen(req, timeout=20, context=ctx)
        body = r.read(400)
        print(f'[{name}] {r.status} {len(body)}B')
        print(f'    {body[:200]!r}')
    except urllib.error.HTTPError as e:
        b = e.read(200)
        print(f'[{name}] HTTP {e.code}')
        print(f'    {b[:150]!r}')
    except Exception as e:
        print(f'[{name}] ERR {str(e)[:100]}')