# -*- coding: utf-8 -*-
# 启动早期 dd 抓取: so 就绪后 6s 抓数据段, 滑窗验证 XXTEAUtil 区域
import subprocess, time, struct

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUT = r'C:\Users\20751\tomdump\early_dd_out.txt'
ROUNDS = 4

def sh(args, t=120):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return f'ERR {e}'

logf = open(OUT, 'a', encoding='utf-8')
def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    logf.write(s + '\n'); logf.flush()

# 黄金对
MASK = 0xffffffff
DELTA = 0x9e3779b9
plain = open(r'C:\Users\20751\tomdump\mega_luac\src_common_utils.lua.luac', 'rb').read()
cipher = open(r'C:\Users\20751\tomdump\cdn_pull\package\src\13cae617ab2cff39fbdfa8e88053c9a8\a658279f9b983958149f31e4d8487673\c76a5e84e4bdee527e274ea30c680d79\217a71cb4ce1b6a6193f0dabeaa67ff7.bin', 'rb').read()
cdata = cipher[12:]
n = len(cdata) // 4
ref = plain[:n*4]

def check(key16):
    k = struct.unpack('<4I', key16)
    v = list(struct.unpack('<%dI' % n, cdata))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for p in range(n - 1, 0, -1):
            z = v[p - 1]
            ki = (p ^ e) & 3
            mx = ((((z ^ k[ki]) + (y ^ sumv)) & MASK) ^
                  ((((y >> 3) ^ ((z << 4) & MASK)) + (((y << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[p] = (v[p] - mx) & MASK
            y = v[p]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^
               (((y ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    return struct.pack('<%dI' % n, *v)[:16] == ref[:16]

def grab(pid, s, e, name, t=60):
    page, cnt = s >> 12, (e - s + 4095) >> 12
    dev = f'/data/local/tmp/ed_{name}.bin'
    sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={cnt} of={dev} 2>&1"'], t)
    sh(['pull', dev, rf'C:\Users\20751\tomdump\early_dd\{name}.bin'], t)

import os
os.makedirs(r'C:\Users\20751\tomdump\early_dd', exist_ok=True)
log(f'=== 启动早期抓取 {time.strftime("%H:%M:%S")} ===')
for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    pid = None
    for _ in range(40):
        time.sleep(1)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit(): break
    if not pid.isdigit():
        log('  启动失败'); continue
    # so 就绪 + 6s (解密期)
    for _ in range(30):
        so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
        if so.isdigit() and int(so) > 0: break
        time.sleep(1)
    time.sleep(6)
    alive = sh(['shell', 'pidof com.netease.tom']).isdigit()
    log(f'  PID={pid} 存活={alive}')
    # 抓固定数据段 (so rw)
    grab(pid, 0x400021d74000, 0x4000222e2000, f'r{rnd}_sd')
    # 抓 rw 匿名段 (probe)
    maps = sh(['shell', f'cat /proc/{pid}/maps'])
    for l in maps.splitlines():
        p = l.split()
        if len(p) < 2: continue
        s, e = p[0].split('-')
        s, e = int(s, 16), int(e, 16)
        if 'rw' in p[1] and 0x700000000000 <= s <= 0x800000000000 and 0x400000 <= e - s <= 0x2000000:
            grab(pid, s, e, f'r{rnd}_{s & 0xfffff:x}', t=120)
    log(f'  抓取完成, 验证 XXTEAUtil 区域...')
    # 滑窗验证 so rw 段
    b = open(rf'C:\Users\20751\tomdump\early_dd\r{rnd}_sd.bin', 'rb').read()
    # XXTEAUtil 镜像偏移 0x158ae00 → sodata 内偏移 0x158ae00-0x1074000 = 0x516e00
    for base in [0x516e00 - 0x800, 0x516e00]:
        for i in range(base, min(base + 0x2000, len(b) - 16)):
            if check(b[i:i+16]):
                log(f'  ★★★ KEY 命中 @sodata+{hex(i)}: {b[i:i+16].hex()}')
                open(r'C:\Users\20751\tomdump\KEY_FOUND.bin', 'wb').write(b[i:i+16])
                logf.close()
                raise SystemExit
    log('  XXTEAUtil 区域无命中')
    # 验证新抓的匿名段
    for fn in os.listdir(r'C:\Users\20751\tomdump\early_dd'):
        if fn.startswith(f'r{rnd}_') and fn != f'r{rnd}_sd.bin':
            bb = open(rf'C:\Users\20751\tomdump\early_dd\{fn}', 'rb').read()
            nx = bb.count(b'X1V5fzTo')
            if nx:
                log(f'  {fn}: X1={nx} 滑窗验证前 1MB...')
                for i in range(0, min(len(bb) - 16, 0x100000)):
                    if check(bb[i:i+16]):
                        log(f'  ★★★ KEY 命中 @{fn}+{hex(i)}: {bb[i:i+16].hex()}')
                        open(r'C:\Users\20751\tomdump\KEY_FOUND.bin', 'wb').write(bb[i:i+16])
                        logf.close()
                        raise SystemExit
log('=== 结束 ===')
logf.close()
