# -*- coding: utf-8 -*-
"""整理 rev_all: 按 source 路径重命名反编译输出 → 项目结构 + 索引"""
import os, re, glob, shutil

REV = r'C:\Users\20751\Desktop\猫和老鼠\PLAINS\rev_all'
DST = r'C:\Users\20751\Desktop\猫和老鼠\tom_scripts'
os.makedirs(DST, exist_ok=True)

index = []
no_src = []
for f in glob.glob(os.path.join(REV, '*.lua')):
    txt = open(f, encoding='utf-8', errors='replace').read()
    # fn#0 的源路径: "fn#0 '@src/...' (N instr"
    m = re.search(r"fn#0 '([^']*)'", txt)
    src = m.group(1) if m else ''
    if src.startswith('@src/'):
        rel = src[5:]  # 去 @src/
        dst = os.path.join(DST, rel)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copy(f, dst)
        index.append((rel, os.path.getsize(f)))
    else:
        no_src.append((os.path.basename(f), src, len(txt)))

# 索引
with open(os.path.join(DST, 'INDEX.md'), 'w', encoding='utf-8') as w:
    w.write('# 猫和老鼠明文脚本索引 (2026-08-16 捕获反编译)\n\n')
    w.write(f'共 {len(index)} 个脚本 + {len(no_src)} 个未命名\n\n')
    for rel, sz in sorted(index):
        w.write(f'- `{rel}` ({sz}B)\n')
    w.write('\n## 未命名\n')
    for b, s, sz in no_src:
        w.write(f'- {b} src={s!r} ({sz}B)\n')

print('organized:', len(index))
print('no_src:', no_src[:8])
print('DST:', DST)