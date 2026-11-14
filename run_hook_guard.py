# -*- coding: utf-8 -*-
# 守护版: 游戏检测 + 自动重启 + hook_alldelta 抓启动解密
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_alldelta.js'
OUT = r'C:\Users\20751\tomdump\hook_guard_out.txt'
MAX_ROUNDS = 8

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

def start_game():
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    for _ in range(45):
        time.sleep(1)
        p = game_pid()
        if p:
            return p
    return None

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== 守护版 {time.strftime("%H:%M:%S")} ===')

for rnd in range(1, MAX_ROUNDS + 1):
    log('--- 轮 %d ---' % rnd)
    sh(['shell', 'su -c "rm -f /data/data/com.netease.tom/files/hooklog.txt"'])

    pid = game_pid()
    if not pid:
        log('  [守护] 游戏未运行, 启动...')
        pid = start_game()
        if not pid:
            log('  [!] 启动失败, 30s 后重试')
            time.sleep(30)
            continue
    log('  [守护] 游戏 PID=%s' % pid)

    t0 = time.time()
    ready = False
    while time.time() - t0 < 60:
        if not game_pid():
            log('  [守护] 游戏等待期死亡, 重启')
            break
        maps = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null'])
        if 'rwx' in maps and ('779' in maps or '3fff' in maps or '40006' in maps):
            ready = True
            break
        time.sleep(1)
    if not ready:
        if game_pid():
            log('  转译 60s 未就绪, 下轮')
        continue
    log('  转译就绪 (%.0fs)' % (time.time() - t0))

    try:
        session = dev.attach(int(pid))
        log('  attach OK')
    except Exception as e:
        log('  attach 失败: %s' % e)
        log('  [守护] 强制重启游戏')
        sh(['shell', 'am force-stop com.netease.tom'])
        time.sleep(3)
        continue
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', lambda m, d: None)
    try:
        script.load()
        log('  hook 已加载')
    except Exception as e:
        log('  脚本失败: %s' % e)
        try: session.detach()
        except Exception: pass
        continue

    seen = set()
    t_end = time.time() + 150
    got = False
    while time.time() < t_end:
        time.sleep(5)
        if not game_pid():
            log('  [守护] 游戏死亡, 下轮重启')
            break
        hl = read_log()
        for line in hl.splitlines():
            if line not in seen:
                seen.add(line)
                log('    |', line)
        if '[★K]' in hl or '[★MEM' in hl:
            log('  [HIT] key 候选!!')
            got = True
            break
    log('  轮 %d 结束 (%s)' % (rnd, '命中!' if got else '无'))
    try: session.detach()
    except Exception: pass
    if got:
        break
log('=== 结束 ===')
logf.close()
