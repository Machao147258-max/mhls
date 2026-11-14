# -*- coding: utf-8 -*-
# 并发解析 乱码_0 + 数字编号 APK 包名 (8 线程)
import os, re, subprocess, json
from concurrent.futures import ThreadPoolExecutor

d = r'D:\ai测试\app\软件站\总和'
aapt = r'D:\androidsdk\Sdk\build-tools\34.0.0\aapt.exe'

apks = [f for f in os.listdir(d) if f.endswith('.apk')]
targets = [f for f in apks if ('_0.apk' in f and not any(c.isascii() and c.isalnum() for c in f.split('_')[0])) or re.match(r'^\d+_\d+\.apk$', f)]
print('待解析:', len(targets))

def get_pkg(f):
    p = os.path.join(d, f)
    try:
        r = subprocess.run([aapt, 'dump', 'badging', p], capture_output=True, timeout=60)
        out = r.stdout.decode('utf-8', 'replace')
        for line in out.splitlines():
            if line.startswith('package:'):
                return f, line.split(' ')[1].split('=')[1].strip("'\"")
        return f, ''
    except Exception:
        return f, 'ERR'

results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    for f, pkg in ex.map(get_pkg, targets):
        results[f] = pkg

json.dump(results, open(r'C:\Users\20751\tomdump\suspect_pkgs.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
valid = set('''app.laidianyi.quanqiuwa club.spss.tagoo com.alimama.moon com.android.yzd.habit com.bantu.trssgshz2.aligames com.chinaclear.fund com.duxiaoman.wallet com.eg.android.AlipayGphone com.fengsu.aicapture com.founder.bysypatientapp com.haodf.android com.haodf.android.doctor com.hnzycfc.zyxj com.ircloud.ydp com.jd.jrapp com.kuailon.wldj com.kuaishou.nebula com.kwai.theater com.liurenyou.im com.lujing.tjjpdpgj com.newdim.partlib.v1 com.phoenix.read com.shejijia.android.designer com.sofunny.Sausage com.sportq.fit com.ss.android.auto com.tencent.KiHan com.tencent.tmgp.cf com.tongcheng.android com.wildsky.td com.xunmeng.pinduoduo com.yitong.zjrc.mfs.android com.yyb.shop com.zengame.hlmjhdj.HUAWEI com.zhan.ieltstiku com.zhipu.agent com.zhongheschool.online insigma.waybook.jinan me.weishu.kernelsu org.zzmetro.eticket'''.split())
keep, delete, fail = [], [], []
for f, pkg in results.items():
    if pkg in valid:
        keep.append((f, pkg))
    elif pkg in ('', 'ERR'):
        fail.append((f, pkg))
    else:
        delete.append((f, pkg))
print('匹配有效(保留):', len(keep))
for f, p in keep:
    print('  OK', p, '←', f[:50])
print('解析失败(垃圾):', len(fail))
print('其他包(删):', len(delete))
for f, p in sorted(delete)[:40]:
    print('  DEL', p[:40], '←', f[:50])
json.dump({'keep': keep, 'delete': delete, 'fail': fail}, open(r'C:\Users\20751\tomdump\suspect_class.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
