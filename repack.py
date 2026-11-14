# -*- coding: utf-8 -*-
# 通用模块打包（正斜杠）: python repack.py <模块zip> [输出名]
import zipfile, os, sys, tempfile, shutil

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
    print('OK:', out_path, n, 'files', os.path.getsize(out_path), 'bytes')

if len(sys.argv) >= 3:
    src = sys.argv[1]
    out = sys.argv[2]
else:
    src = r'D:\汇总\mumu必刷\hide_mumu_files.zip'
    out = r'D:\汇总\mumu必刷\hide_mumu_files_fixed.zip'

tmp = tempfile.mkdtemp()
try:
    unpack(src, tmp)
    repack(tmp, out)
finally:
    shutil.rmtree(tmp, ignore_errors=True)