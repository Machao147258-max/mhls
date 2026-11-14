# -*- coding: utf-8 -*-
# 稳定 attach + 正确地址 hook + 点击触发 (每轮 90s)
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_maps2.js'
OUT = r'C:\Users\20751\tomdump\hook_stable2_out.txt'
ROUNDS = 5

def sh(args, t=30):
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

def read_log():
    return sh(['shell', 'su -c "cat /data/data/com.netease.tom/files/hooklog.txt 2>/dev/null"'])

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== 稳定+正确地址 {time.strftime("%H:%M:%S")} ===')
for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    sh(['shell', 'su -c "rm -f /data/data/com.netease.tom/files/hooklog.txt"'])
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    pid = None
    for _ in range(45):
        time.sleep(1)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit(): break
    if not pid.isdigit():
        log('  启动失败'); continue
    t0 = time.time()
    dead = False
    while time.time() - t0 < 55:
        time.sleep(5)
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            dead = True; break
    if dead:
        log('  未稳定'); continue
    log(f'  稳定 PID={pid}')
    try:
        session = dev.attach(int(pid))
        log('  attach OK')
    except Exception as e:
        log(f'  attach 失败: {e}'); continue
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', lambda m, d: None)
    try:
        script.load()
        log('  hook 已装')
    except Exception as e:
        log(f'  脚本失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    time.sleep(3)
    hl = read_log()
    for line in hl.splitlines():
        log('  |', line)
    # 点击触发
    taps = [(540,1000),(540,1150),(540,1300),(540,800),(270,900),(810,900),
            (540,600),(270,1400),(810,1400),(540,1700),(540,1450),(540,700)]
    tap_i = 0
    t_end = time.time() + 85
    last = ''
    while time.time() < t_end:
        x, y = taps[tap_i % len(taps)]
        tap_i += 1
        sh(['shell', f'input tap {x} {y}'])
        time.sleep(3)
        hl = read_log()
        if hl != last:
            for line in hl.splitlines():
                if line not in last.splitlines():
                    log('  |', line)
            last = hl
        if '[★decwrap]' in hl:
            log('  [★★★] 抓到 key!!')
            logf.close()
            raise SystemExit
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            log(f'  游戏死亡 (点击 {tap_i})')
            break
    log(f'  轮 {rnd} 结束')
    try: session.detach()
    except Exception: pass
log('=== 结束 ===')
logf.close()
