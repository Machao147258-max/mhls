# -*- coding: utf-8 -*-
# 重启触发: 启动早期 attach + boot2 hook, 自动重试直到抓到 key
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_boot2.js'
OUT = r'C:\Users\20751\tomdump\boot2_out.txt'
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

def game_pid():
    p = sh(['shell', 'pidof com.netease.tom'])
    return p if p.isdigit() else None

def start():
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    for _ in range(40):
        time.sleep(1)
        p = game_pid()
        if p:
            return p
    return None

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45679')
log(f'=== 启动触发 {time.strftime("%H:%M:%S")} ===')
for rnd in range(1, ROUNDS + 1):
    log('--- 轮 %d ---' % rnd)
    sh(['shell', 'su -c "rm -f /data/data/com.netease.tom/files/hooklog.txt"'])
    pid = start()
    if not pid:
        log('  启动失败')
        continue
    log('  pid=%s' % pid)
    # 等 8s (进程稳定但还在加载)
    time.sleep(8)
    try:
        session = dev.attach(int(pid))
        log('  attach OK (加载期)')
    except Exception as e:
        log('  attach 失败: %s' % e)
        sh(['shell', 'am force-stop com.netease.tom'])
        continue
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', lambda m, d: None)
    try:
        script.load()
        log('  hook 加载')
    except Exception as e:
        log('  脚本失败: %s' % e)
        try: session.detach()
        except Exception: pass
        continue
    # 观察 120s
    seen = set()
    t_end = time.time() + 120
    got = False
    while time.time() < t_end:
        time.sleep(5)
        if not game_pid():
            log('  [守护] 游戏死亡')
            break
        hl = read_log()
        for line in (hl or '').splitlines():
            if line not in seen:
                seen.add(line)
                log('  |', line)
        if '[★K' in hl:
            log('  ★ KEY!!')
            got = True
            break
    log('  轮 %d 结束 (%s)' % (rnd, '命中!' if got else '无'))
    try: session.detach()
    except Exception: pass
    if got:
        break
log('=== 结束 ===')
logf.close()
