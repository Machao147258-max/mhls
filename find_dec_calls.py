# -*- coding: utf-8 -*-
# 解密链静态分析: 找所有调用 0x85261c(解密包装) 的函数, 看 key 参数(x2)来源
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

so = open(r'C:\Users\20751\tomdump\device_libs\libcocos2dlua_RUNTIME.so', 'rb').read()
md = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
md.detail = True

TARGETS = {0x85261c: 'decwrap', 0x852548: 'reader', 0x4095b0: 'luadec_reg', 0x408ddc: 'luaenc_reg'}
TARGET_OFF = {t: t - 0x85261c for t in TARGETS}
# 搜索 bl 指令目标 (imm26)
calls = {t: [] for t in TARGETS}
for ins in md.disasm(so, 0):
    if ins.mnemonic == 'bl':
        try:
            target = ins.operands[0].imm
        except Exception:
            continue
        if target in TARGETS:
            calls[target].append(ins.address)
print('=== bl 调用点 ===')
for t, name in TARGETS.items():
    print(f'{name} @0x{t:x}: {len(calls[t])} 个调用者')
    for a in calls[t][:20]:
        print(f'   0x{a:x}')
