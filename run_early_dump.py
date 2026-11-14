# -*- coding: utf-8 -*-
# 启动早期抓取循环: 启动游戏 → so 加载后立即 dd 抓命中段 + 堆 → 分析新增内容
# 每轮: 闪退与否都抓 (启动早期内存最热)
import subprocess, time, os, re, struct, glob

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
ROUNDS = 4
KEY1 = bytes.fromhex('6bb4c7d132b432820cc35d8e6cc76c6b')

def sh(args, t=60):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return f'ERR {e}'

def dump_seg(pid, s, e, name):
    page, n = s >> 12, (e - s + 4095) >> 12
    dev = f'/data/local/tmp/early_{name}.bin'
    sh(['shell', f'su -c "dd if=/proc/{pid}/mem bs=4096 skip={page} count={n} of={dev} 2>&1"'], t=300)
    sh(['pull', dev, rf'C:\Users\20751\tomdump\early\{name}.bin'], t=300)

os.makedirs(r'C:\Users\20751\tomdump\early', exist_ok=True)
logf = open(r'C:\Users\20751\tomdump\early_log.txt', 'a', encoding='utf-8')
def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    logf.write(s + '\n'); logf.flush()

log(f'=== 启动早期抓取 {time.strftime("%H:%M:%S")} ===')
for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(3)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    pid = None
    t0 = time.time()
    while time.time() - t0 < 45:
        out = sh(['shell', 'pidof com.netease.tom'])
        if out.isdigit():
            pid = out
            break
        time.sleep(0.3)
    if not pid:
        log('[-] 未启动')
        continue
    # 等 so 加载
    t0 = time.time()
    while time.time() - t0 < 60:
        out = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
        if out.isdigit() and int(out) > 0:
            break
        time.sleep(0.2)
    so_t = time.time() - t0
    log(f'[+] PID={pid} so 加载于 {so_t:.1f}s')
    # 等 3 秒 (解密高峰期), 然后抓取
    time.sleep(3)
    # 抓命中段 + 堆 (probe 已知 + 常见堆)
    segs = [
        (0x778eba697000, 0x778eba7d7000, 'x1'),
        (0x77904a6d5000, 0x77904a815000, 'x2'),
        (0x778e90600000, 0x778e9c600000, 'heap192'),
    ]
    for s, e, name in segs:
        try:
            dump_seg(pid, s, e, f'r{rnd}_{name}')
            log(f'  抓取 {name} OK')
        except Exception as ex:
            log(f'  抓取 {name} 失败: {ex}')
    # 立即分析
    for fn in sorted(glob.glob(rf'C:\Users\20751\tomdump\early\r{rnd}_*.bin')):
        b = open(fn, 'rb').read()
        n_x = b.count(b'X1V5fzTo')
        n_l = b.count(b'\x1bLuaQ')
        k1 = b.find(KEY1)
        log(f'  {os.path.basename(fn)}: {len(b)}B X1={n_x} luac={n_l} KEY1={hex(k1) if k1>=0 else "NO"}')
    # 检查游戏是否还活着
    alive = sh(['shell', f'pidof com.netease.tom']).isdigit()
    log(f'  游戏存活: {alive}')
    if alive:
        log('  [+] 游戏存活, 继续等 30s 让更多解密发生再抓一轮')
        time.sleep(30)
        for s, e, name in segs:
            try:
                dump_seg(pid, s, e, f'r{rnd}b_{name}')
                log(f'  第二轮抓取 {name} OK')
            except Exception as ex:
                log(f'  第二轮抓取失败: {ex}')
        for fn in sorted(glob.glob(rf'C:\Users\20751\tomdump\early\r{rnd}b_*.bin')):
            b = open(fn, 'rb').read()
            n_x = b.count(b'X1V5fzTo')
            n_l = b.count(b'\x1bLuaQ')
            k1 = b.find(KEY1)
            log(f'  {os.path.basename(fn)}: {len(b)}B X1={n_x} luac={n_l} KEY1={hex(k1) if k1>=0 else "NO"}')
log('=== 结束 ===')
logf.close()
