# -*- coding: utf-8 -*-
# 自然启动 → 稳定 attach → hook_scan(自动定位 keyload) → 点击触发
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_scan.js'
OUT = r'C:\Users\20751\tomdump\hook_scan2_out.txt'
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
log(f'=== 自然启动+自动扫描 {time.strftime("%H:%M:%S")} ===')
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
    # 稳定检查: 90s 存活 + 屏幕亮度 (非黑屏)
    t0 = time.time()
    alive_ok = False
    while time.time() - t0 < 90:
        time.sleep(6)
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            break
        if time.time() - t0 > 40:
            # 亮度检查
            sh(['shell', 'screencap -p /data/local/tmp/sc.png'])
            try:
                from PIL import Image
                img = Image.open(r'C:\Users\20751\tomdump\sc.png').convert('RGB').resize((16, 16))
                px = list(img.getdata())
                avg = sum(sum(p) for p in px) / (len(px) * 3)
                if avg > 30:
                    alive_ok = True
                    log(f'  屏幕亮度 {avg:.0f} (界面活跃)')
                    break
            except Exception:
                pass
    if not alive_ok:
        log('  未稳定(黑屏/死亡)'); continue
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
        log('  扫描脚本已加载')
    except Exception as e:
        log(f'  脚本失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    # 等待扫描完成 (hook 就绪)
    t0 = time.time()
    hooked = False
    while time.time() - t0 < 60:
        time.sleep(2)
        hl = read_log()
        if 'keyload hook' in hl or 'keyload2 hook' in hl:
            hooked = True
            log('  [OK] keyload hook 就绪!')
            for line in hl.splitlines():
                if 'DELTA' in line or 'KEYLOAD' in line or 'hook' in line:
                    log('    |', line)
            break
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            log('  游戏死亡(扫描期)'); break
    if not hooked:
        log('  [!] 60s 未定位到 keyload')
        try: session.detach()
        except Exception: pass
        continue
    # 点击触发 (开始游戏/商店/活动/匹配)
    seq = [(540,1150),(540,1200),(540,1300),(540,1400),(540,1000),(540,1500),
           (900,800),(900,1000),(900,1200),(180,1000),(540,1700),(540,900),
           (540,500),(540,700),(270,600),(810,600),(540,1600),(540,300)]
    seen = set()
    tap_i = 0
    t_end = time.time() + 120
    while time.time() < t_end:
        x, y = seq[tap_i % len(seq)]
        tap_i += 1
        sh(['shell', f'input tap {x} {y}'])
        time.sleep(3)
        hl = read_log()
        for line in hl.splitlines():
            if line not in seen:
                seen.add(line)
                log('    |', line)
        if '[★★★KEY]' in hl:
            log('  [HIT] KEY 到手!!')
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
