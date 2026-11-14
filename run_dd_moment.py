# -*- coding: utf-8 -*-
# 解密瞬间 dd: so 就绪 +1.5s 抓 rwxp 段 + 周边堆, 精确黄金对滑窗
import subprocess, time, struct, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUT = r'C:\Users\20751\tomdump\dd_moment_out.txt'
ROUNDS = 5

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

# 精确黄金对 UGCSystem
MASK = 0xffffffff
DELTA = 0x9e3779b9
c = open(r'C:\Users\20751\tomdump\pair2\UGCSystem.bin', 'rb').read()
p = open(r'C:\Users\20751\tomdump\mega_luac\src_catchGame_systems_UGCSystem.lua.luac', 'rb').read()
def check(key16):
    cdata = c[12:][:len(c[12:])//4*4]
    n = len(cdata)//4
    k = struct.unpack('<4I', key16)
    v = list(struct.unpack('<%dI' % n, cdata))
    rounds = 6 + 52 // n
    sumv = (rounds * DELTA) & MASK
    while sumv != 0:
        e = sumv >> 2
        y = v[0]
        for i in range(n - 1, 0, -1):
            z = v[i - 1]
            ki = (i ^ e) & 3
            mx = ((((z ^ k[ki]) + (y ^ sumv)) & MASK) ^ ((((y >> 3) ^ ((z << 4) & MASK)) + (((y << 2) & MASK) ^ (z >> 5))) & MASK)) & MASK
            v[i] = (v[i] - mx) & MASK
            y = v[i]
        z = v[n - 1]
        ki = e & 3
        mx0 = (((((z >> 5) ^ ((y << 2) & MASK)) + (((z << 4) & MASK) ^ (y >> 3))) & MASK) ^ (((y ^ sumv) + (z ^ k[ki])) & MASK)) & MASK
        v[0] = (v[0] - mx0) & MASK
        sumv = (sumv - DELTA) & MASK
    out = struct.pack('<%dI' % n, *v)
    return sum(1 for a, b in zip(out[:64], p[:64]) if a == b) > 48

def grab(pid, s, e, name):
    page, cnt = s >> 12, (e - s + 4095) >> 12
    dev = f'/data/local/tmp/dm_{name}.bin'
    sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={cnt} of={dev} 2>&1"'], t=90)
    sh(['pull', dev, rf'C:\Users\20751\tomdump\dd_moment\{name}.bin'], t=90)

os.makedirs(r'C:\Users\20751\tomdump\dd_moment', exist_ok=True)
log(f'=== 解密瞬间 dd {time.strftime("%H:%M:%S")} ===')
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
    # so 就绪
    t0 = time.time()
    for _ in range(40):
        so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c 400021652'])
        if so.isdigit() and int(so) > 0: break
        time.sleep(0.5)
    log(f'  so 就绪 {(time.time()-t0)*1000:.0f}ms')
    time.sleep(1.5)  # 解密瞬间
    # 抓 rwxp 段 + 周边堆
    maps = sh(['shell', f'cat /proc/{pid}/maps'])
    rwx = []
    for l in maps.splitlines():
        pp = l.split()
        if len(pp) < 2: continue
        s, e = pp[0].split('-')
        s, e = int(s, 16), int(e, 16)
        if 'rwx' in pp[1] and 0x700000000000 <= s <= 0x800000000000:
            rwx.append((s, e))
    log(f'  rwx 段 {len(rwx)}: {[hex(x[0]) for x in rwx[:6]]}')
    for s, e in rwx[:6]:
        if e - s < 0x100000:
            grab(pid, s, e, f'r{rnd}_{s & 0xfffff:x}')
    # 滑窗验证
    for fn in os.listdir(r'C:\Users\20751\tomdump\dd_moment'):
        if not fn.startswith(f'r{rnd}_'): continue
        b = open(rf'C:\Users\20751\tomdump\dd_moment\{fn}', 'rb').read()
        if len(b) < 16: continue
        for i in range(0, len(b) - 16):
            if check(b[i:i+16]):
                log(f'  ★★★ KEY @{fn}+{hex(i)}: {b[i:i+16].hex()}')
                open(r'C:\Users\20751\tomdump\KEY_FOUND.bin', 'wb').write(b[i:i+16])
                logf.close()
                raise SystemExit
    log(f'  轮 {rnd}: rwx 段滑窗无命中')
    # 游戏状态
    log(f'  游戏存活: {sh(["shell", "pidof com.netease.tom"]).isdigit()}')
log('=== 结束 ===')
logf.close()
