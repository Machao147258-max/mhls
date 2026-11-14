# -*- coding: utf-8 -*-
# 重新打包 nosuke 模块（正斜杠路径，Android 兼容）
import zipfile, os

src = r'D:\汇总\新frida\frida面具模块'
out = r'D:\汇总\新frida\nosuke-module-fixed.zip'
if os.path.exists(out):
    os.remove(out)
count = 0
with zipfile.ZipFile(out, 'w', zipfile.ZIP_DEFLATED) as z:
    for root, dirs, files in os.walk(src):
        for f in files:
            p = os.path.join(root, f)
            rel = os.path.relpath(p, src).replace('\\', '/')
            z.write(p, rel)
            count += 1
            print('  +', rel)
print('打包完成:', out, count, '个文件', os.path.getsize(out), '字节')
