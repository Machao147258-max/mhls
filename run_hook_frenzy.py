# -*- coding: utf-8 -*-
# 疯狂触发驱动: attach 后密集点击, 死亡重启, 循环直到抓 key
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_maps.js'
OUT = r'C:\Users\20751\tomdump\hook_frenzy_out.txt'
CYCLES = 8

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

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== 疯狂触发 {time.strftime("%H:%M:%S")} ===')

taps = [(540,960),(540,1200),(540,1500),(540,600),(900,1700),(540,900),
        (270,480),(810,480),(540,300),(540,1700),(270,1500),(810,1500),
        (540,100),(900,300),(180,900),(900,900),(540,1400),(540,700)]

for cyc in range(1, CYCLES + 1):
    log(f'--- 周期 {cyc} ---')
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
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
        continue
    # 等 so 加载
    t0 = time.time()
    while time.time() - t0 < 60:
        so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
        if so.isdigit() and int(so) > 0:
            break
        time.sleep(0.3)
    # attach (不等稳定, so 加载后立即)
    try:
        session = dev.attach(int(pid))
        log(f'[+] attach {pid}')
    except Exception as e:
        log(f'[-] attach 失败: {e}')
        continue
    msgs = []
    def on_message(msg, data):
        t = msg.get('type')
        if t == 'send': msgs.append(str(msg['payload']))
        elif t == 'log': msgs.append(str(msg.get('payload', '')))
        elif t == 'error': msgs.append('ERR: ' + str(msg.get('stack', ''))[:200])
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', on_message)
    try:
        script.load()
        log('[+] hook 已装')
    except Exception as e:
        log(f'[-] 脚本失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    # 疯狂点击 60 秒 (短窗口, 快速反馈)
    tap_i = 0
    last_out = 0
    t_end = time.time() + 60
    while time.time() < t_end:
        x, y = taps[tap_i % len(taps)]
        tap_i += 1
        sh(['shell', f'input tap {x} {y}'])
        time.sleep(2)
        for m in msgs[last_out:]:
            log('  |', m)
        last_out = len(msgs)
        if '[★' in '\n'.join(msgs):
            log('[★] 命中 key!!')
            for m in msgs:
                log('FINAL |', m)
            logf.close()
            raise SystemExit
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            log(f'[-] 游戏死亡 (点击 {tap_i} 次)')
            break
    try: session.detach()
    except Exception: pass
log('=== 结束 ===')
logf.close()
