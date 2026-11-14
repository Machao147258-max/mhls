# -*- coding: utf-8 -*-
# 顺序解析 (index 唯一临时名)
import os, re, subprocess, json, shutil

d = r'D:\ai测试\app\软件站\总和'
aapt = r'D:\androidsdk\Sdk\build-tools\34.0.0\aapt.exe'
tmp = r'C:\Users\20751\tomdump\aptmp'
os.makedirs(tmp, exist_ok=True)

apks = [f for f in os.listdir(d) if f.endswith('.apk')]
targets = [f for f in apks if ('_0.apk' in f and not any(c.isascii() and c.isalnum() for c in f.split('_')[0])) or re.match(r'^\d+_\d+\.apk$', f)]
print('待解析:', len(targets))

results = {}
for idx, f in enumerate(targets):
    t = os.path.join(tmp, 'a%d.apk' % idx)
    try:
        shutil.copy2(os.path.join(d, f), t)
        r = subprocess.run([aapt, 'dump', 'badging', t], capture_output=True, timeout=90)
        os.remove(t)
        out = r.stdout.decode('utf-8', 'replace')
        pkg = ''
        for line in out.splitlines():
            if line.startswith('package:'):
                pkg = line.split(' ')[1].split('=')[1].strip("'\"")
                break
        results[f] = pkg
    except Exception as e:
        results[f] = 'ERR'
    if idx % 25 == 0:
        print('...%d/%d' % (idx, len(targets)), flush=True)

json.dump(results, open(r'C:\Users\20751\tomdump\suspect_pkgs3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
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
print('解析成功但非有效(可删):', len(delete))
for f, p in sorted(delete):
    print('  DEL', p[:44], '←', f[:50])
print('解析失败(损坏):', len(fail))
json.dump({'keep': keep, 'delete': delete, 'fail': fail}, open(r'C:\Users\20751\tomdump\suspect_class3.json', 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
