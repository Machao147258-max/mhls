# -*- coding: utf-8 -*-
# 直接从原始内存段 s631.bin @0x748 解析 launcher.lua luac 并反汇编
import struct, sys
sys.path.insert(0, r'C:\Users\20751\Desktop\猫和老鼠')
import vm_disasm_engine as V

buf = open(r'C:\Users\20751\tomdump\dd_live_1973\s631.bin', 'rb').read()
print(f's631.bin = {len(buf)}B')

for start in (0x748, 0x754, 0x740, 0x74c, 0x750):
    lines = []
    try:
        end, info = V.parse_proto(buf, start, 0, lines)
        if end is not None:
            print(f'✓ start=0x{start:x} end=0x{end:x} ({end-start}B) 行数={len(lines)}')
            open(r'C:\Users\20751\tomdump\launcher_raw.asm', 'w', encoding='utf-8').write('\n'.join(lines))
            print('已存 launcher_raw.asm')
            break
        else:
            print(f'✗ start=0x{start:x} 解析失败')
    except Exception as e:
        print(f'✗ start=0x{start:x} 异常 {e}')
