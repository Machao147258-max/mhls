# -*- coding: utf-8 -*-
# attach 稳定游戏 → hook → 删 hotfix/缓存 → 触发重载 → 抓解密 key
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key5.js'
OUT = r'C:\Users\20751\tomdump\hook_reload2_out.txt'
ROUNDS = 4

def sh(args, t=20):
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

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== 删文件重载 {time.strftime("%H:%M:%S")} ===')

for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    # 启动游戏 (自然启动)
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    pid = None
    for _ in range(45):
        time.sleep(1)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit(): break
    if not pid.isdigit():
        log('  启动失败')
        continue
    # 等 60s 稳定
    t0 = time.time()
    dead = False
    while time.time() - t0 < 60:
        time.sleep(5)
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            dead = True
            break
    if dead:
        log('  未稳定, 下轮')
        continue
    log(f'  稳定 PID={pid}')
    # attach
    try:
        session = dev.attach(int(pid))
        log('  attach OK')
    except Exception as e:
        log(f'  attach 失败: {e}')
        continue
    msgs = []
    def on_message(msg, data):
        t = msg.get('type')
        if t in ('send', 'log'):
            msgs.append(str(msg.get('payload', '')))
        elif t == 'error':
            msgs.append('ERR ' + str(msg.get('stack', ''))[:150])
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', on_message)
    try:
        script.load()
        log('  hook 已装')
    except Exception as e:
        log(f'  脚本失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    time.sleep(2)
    # 删文件 (热更 + 已下载资源)
    for f in [
        '/data/data/com.netease.tom/files/hotfix/hotfix_battle',
        '/data/data/com.netease.tom/files/hotfix/hotfix_list',
        '/data/data/com.netease.tom/files/filelist_high.json',
        '/data/data/com.netease.tom/files/launcher_version.json',
    ]:
        sh(['shell', f'su -c "rm -f {f} 2>/dev/null"'])
    log('  已删热更/缓存文件')
    # 点击触发 (设置/重载相关区域) + 观察 90s
    taps = [(540,1500),(540,1200),(900,300),(540,960),(810,100),(270,1600),(540,600)]
    last = 0
    tap_i = 0
    t_end = time.time() + 90
    while time.time() < t_end:
        x, y = taps[tap_i % len(taps)]
        tap_i += 1
        sh(['shell', f'input tap {x} {y}'])
        time.sleep(3)
        if len(msgs) > last:
            for m in msgs[last:]:
                log('    |', m)
            last = len(msgs)
        if '[★' in '\n'.join(msgs):
            log('  [★] 命中 key!!')
            for m in msgs: log('    FINAL |', m)
            logf.close()
            raise SystemExit
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            log(f'  游戏死亡 (点击 {tap_i})')
            break
    log(f'  轮 {rnd} 结束, {len(msgs)} 条')
    try: session.detach()
    except Exception: pass
log('=== 结束 ===')
logf.close()
