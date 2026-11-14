# -*- coding: utf-8 -*-
# 扫描安全 SDK 检测特征
import os, re, sys

base = r'C:\Users\20751\Desktop\猫和老鼠\lib_arm64\tom_lib'
targets = ['libsecsdk.so', 'libsec-lib.so', 'libunisec.so', 'libybuaxz.so', 'libNgModules.so', 'libxdl.so']

# 检测特征关键词
pats = {
    'frida': [r'frida', r'gum-js', r'27042', r'frida-server', r'frida-agent', r'gmain', r'gum_', r'linjector'],
    '调试': [r'ptrace', r'TracerPid', r'debuggerd', r'gdb', r'gdbserver', r'PR_SET_DUMPABLE', r'/proc/self/status', r'anti.?debug'],
    'root': [r'/su\b', r'which su', r'magisk', r'busybox', r'/system/xbin/su', r'Superuser', r'kingroot', r'26657', r'zygisk'],
    'hook': [r'xposed', r'Xposed', r'LSPosed', r'cydia', r'substrate', r'shadow', r'dexposed', r'magisk'],
    '模拟器': [r'nemu', r'qemu', r'goldfish', r'ranchu', r'emulator', r'MuMu', r'bluestacks', r'vbox', r'/dev/socket/qemud'],
    '内核/驱动': [r'kalser', r'rwproc', r'/dev/', r'proc/', r'SELinux', r'kernel'],
    '检测特征': [r'isDebug', r'is_root', r'isEmulator', r'checkSafe', r'anticheat', r'security', r'jailbreak'],
}

def strings(path, minlen=4):
    out = []
    try:
        data = open(path, 'rb').read()
        # ascii 串
        for m in re.finditer(rb'[\x20-\x7e]{%d,}' % minlen, data):
            out.append(m.group().decode('latin-1'))
        # utf16 (常见配置)
        for m in re.finditer(rb'(?:[\x20-\x7e]\x00){4,}', data):
            s = m.group().decode('utf-16-le', errors='ignore')
            if s.isprintable() and len(s) >= 4:
                out.append(s)
    except Exception as e:
        print('err', path, e)
    return out

for t in targets:
    p = base + '\\' + t
    try:
        ss = strings(p)
        print('=' * 30, t, f'({len(ss)} strings)')
        for cat, ps in pats.items():
            hits = set()
            for s in ss:
                for pr in ps:
                    if re.search(pr, s, re.IGNORECASE):
                        hits.add(s)
                        break
            if hits:
                print(f'  [{cat}] {len(hits)} 个:')
                for h in sorted(hits)[:12]:
                    print('    ·', h[:110])
    except FileNotFoundError:
        print(t, '不存在')