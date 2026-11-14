# -*- coding: utf-8 -*-
# 反汇编 VM 主循环取指/分发区
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
SO = r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
out = []
for ins in md.disasm(data[0x6091d4:0x6092c0], 0x6091d4):
    out.append(f'0x{ins.address:06x}: {ins.mnemonic:<8} {ins.op_str}')
open(r'C:\Users\20751\Desktop\猫和老鼠\dispatch.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done', len(out))
