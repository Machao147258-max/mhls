# -*- coding: utf-8 -*-
# 反汇编 encrypt/decrypt 核心与 xor 层, 确认参数结构
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
out = []
def disasm(start, end, label):
    out.append(f'\n===== {label} @0x{start:x} =====')
    for ins in md.disasm(data[start:end], start):
        out.append(f'0x{ins.address:06x}: {ins.mnemonic:<8} {ins.op_str}')

disasm(0x8ab25c, 0x8ab340, 'decrypt 0x8ab25c (entry)')
disasm(0x8ab318, 0x8ab3f0, 'encrypt 0x8ab318 (entry)')
disasm(0x8529c8, 0x852a60, 'xor layer wrapper 0x8529cc')
open(r'C:\Users\20751\Desktop\猫和老鼠\enc_dec_args.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done', len(out))
