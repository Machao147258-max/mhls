# -*- coding: utf-8 -*-
# 批量重打包 mumu必刷 模块（正斜杠路径）
import zipfile, os, tempfile, shutil

base = r'D:\汇总\mumu必刷'
mods = [
    'fix_k40s_board_hardware.zip',
    'fix_k40s_fingerprint.zip',
    'fix_k40s_serial_safe.zip',
    'fix_k40s_telephony_v3.zip',
    'remove_mumu_ads_v5.zip',
]

def unpack(zip_path, dst):
    with zipfile.ZipFile(zip_path) as z:
        z.extractall(dst)

def repack(src_dir, out_path):
    if os.path.exists(out_path):
        os.remove(out_path)
    n = 0
    with zipfile.ZipFile(out_path, 'w', zipfile.ZIP_DEFLATED) as z:
        for root, dirs, files in os.walk(src_dir):
            for f in files:
                p = os.path.join(root, f)
                rel = os.path.relpath(p, src_dir).replace('\\', '/')
                z.write(p, rel)
                n += 1
    print('OK:', os.path.basename(out_path), n, 'files', os.path.getsize(out_path))

for m in mods:
    src = os.path.join(base, m)
    if not os.path.exists(src):
        print('跳过（不存在）:', m)
        continue
    out = os.path.join(base, m.replace('.zip', '_fixed.zip'))
    tmp = tempfile.mkdtemp()
    try:
        unpack(src, tmp)
        repack(tmp, out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)