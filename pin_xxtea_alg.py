# -*- coding: utf-8 -*-
# 反汇编 RUNTIME so 的 XXTEA 区域, 输出到文件
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

SO = r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so'
data = open(SO, 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
out = []
def disasm(start, end, label):
    out.append(f'\n===== {label} @0x{start:x}-0x{end:x} =====')
    for ins in md.disasm(data[start:end], start):
        out.append(f'0x{ins.address:06x}: {ins.mnemonic:<8} {ins.op_str}')

disasm(0x852548, 0x85261c, 'reader 0x852548')
disasm(0x85261c, 0x852804, 'decrypt wrapper+core')
disasm(0x852804, 0x8529c8, 'encrypt core')
disasm(0x8529c8, 0x852a60, 'encrypt dispatcher / xor wrapper')
open(r'C:\Users\20751\Desktop\猫和老鼠\xxtea_disasm.txt', 'w', encoding='utf-8').write('\n'.join(out))
print('done', len(out))
