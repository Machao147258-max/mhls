# -*- coding: utf-8 -*-
# 反汇编块式解密路径: 0x8ab25c 完整 + 0x8ab108 + 0x8b14f4
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM
SO = r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
out = []
def disasm(start, end, label):
    out.append(f'\n===== {label} @0x{start:x} =====')
    for ins in md.disasm(data[start:end], start):
        out.append(f'0x{ins.address:06x}: {ins.mnemonic:<8} {ins.op_str}')

disasm(0x8ab25c, 0x8ab410, '块式解密 0x8ab25c')
disasm(0x8ab108, 0x8ab25c, '块核心 0x8ab108')
disasm(0x8b14f4, 0x8b1600, '辅助 0x8b14f4')
open(r'C:\Users\20751\Desktop\猫和老鼠\block_decrypt.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done', len(out))
