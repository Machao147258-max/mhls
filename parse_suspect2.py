# -*- coding: utf-8 -*-
# 复制到 ASCII 临时路径再解析 (绕 aapt 中文路径 bug)
import os, re, subprocess, json, shutil
from concurrent.futures import ThreadPoolExecutor

d = r'D:\ai测试\app\软件站\总和'
aapt = r'D:\androidsdk\Sdk\build-tools\34.0.0\aapt.exe'
tmp = r'C:\Users\20751\tomdump\aptmp'
os.makedirs(tmp, exist_ok=True)

apks = [f for f in os.listdir(d) if f.endswith('.apk')]
targets = [f for f in apks if ('_0.apk' in f and not any(c.isascii() and c.isalnum() for c in f.split('_')[0])) or re.match(r'^\d+_\d+\.apk$', f)]
print('待解析:', len(targets))

def get_pkg(f):
    try:
        t = os.path.join(tmp, 'a%d.apk' % abs(hash(f)) % 100000)
        shutil.copy2(os.path.join(d, f), t)
        r = subprocess.run([aapt, 'dump', 'badging', t], capture_output=True, timeout=90)
        os.remove(t)
        out = r.stdout.decode('utf-8', 'replace')
        for line in out.splitlines():
            if line.startswith('package:'):
                return f, line.split(' ')[1].split('=')[1].strip("'\"")
        return f, ''
    except Exception as e:
        return f, 'ERR'

results = {}
with ThreadPoolExecutor(max_workers=8) as ex:
    for f, pkg in ex.map(get_pkg, targets):
        results[f] = pkg

json.dump(results, open(r'C:\Users\20751\tomdump\suspect_pkgs2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
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
print()
print('解析成功但非有效(可删):', len(delete))
for f, p in sorted(delete):
    print('  DEL', p[:44], '←', f[:50])
print()
print('解析失败(垃圾/损坏):', len(fail))
json.dump({'keep': keep, 'delete': delete, 'fail': fail}, open(r'C:\Users\20751\tomdump\suspect_class2.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
