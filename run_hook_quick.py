# -*- coding: utf-8 -*-
# 快速 attach 驱动: so 加载后立即 attach + hook_key4 + 重启触发, 输出落盘
import frida, time, subprocess, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key5.js'
OUT = r'C:\Users\20751\tomdump\hook_quick_out.txt'
ROUNDS = 4
WAIT = 100

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

dev = frida.get_device_manager().add_remote_device('127.0.0.1:31337')
log(f'=== 快速 attach 会话 {time.strftime("%H:%M:%S")} ===')

for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    # 等 PID + so (100ms 轮询)
    pid = None
    t0 = time.time()
    while time.time() - t0 < 40:
        out = sh(['shell', 'pidof com.netease.tom'])
        if out.isdigit():
            pid = out
            break
        time.sleep(0.1)
    if not pid:
        log('[-] 无 PID')
        continue
    # 等 so 加载 (快)
    t0 = time.time()
    while time.time() - t0 < 60:
        out = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
        if out.isdigit() and int(out) > 0:
            break
        time.sleep(0.1)
    log(f'[+] PID={pid} so加载耗时 {time.time()-t0:.1f}s')
    # 立即 attach
    try:
        session = dev.attach(int(pid))
        log('[+] attach OK')
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
        log('[+] 脚本加载')
    except Exception as e:
        log(f'[-] 脚本失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    t0 = time.time()
    while time.time() - t0 < WAIT:
        time.sleep(2)
        try:
            script.post({})
        except Exception:
            log('[-] 脚本死亡(闪退?)')
            break
    # 输出
    joined = '\n'.join(msgs)
    for m in msgs:
        log('  |', m)
    logf.flush()
    try: session.detach()
    except Exception: pass
    if '[★' in joined:
        log('[★] 有 key 命中!')
        break
log('=== 结束 ===')
logf.close()
