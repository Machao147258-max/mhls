# -*- coding: utf-8 -*-
# spawn 驱动: dev.spawn 早注入 + hook_key6 (maps 轮询) + resume
import frida, time, subprocess, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key6.js'
OUT = r'C:\Users\20751\tomdump\hook_spawn_out.txt'
ROUNDS = 5
WAIT = 120

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
log(f'=== spawn 会话 {time.strftime("%H:%M:%S")} ===')

for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    try:
        pid = dev.spawn('com.netease.tom')
        log(f'[+] spawn PID={pid}')
    except Exception as e:
        log(f'[-] spawn 失败: {e}')
        continue
    msgs = []
    def on_message(msg, data):
        t = msg.get('type')
        if t == 'send': msgs.append(str(msg['payload']))
        elif t == 'log': msgs.append(str(msg.get('payload', '')))
        elif t == 'error': msgs.append('ERR: ' + str(msg.get('stack', ''))[:300])
    try:
        session = dev.attach(pid)
        script = session.create_script(open(JS, encoding='utf-8').read())
        script.on('message', on_message)
        script.load()
        log('[+] 脚本已加载, resume...')
        dev.resume(pid)
    except Exception as e:
        log(f'[-] 注入失败: {e}')
        try: dev.resume(pid)
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
    for m in msgs:
        log('  |', m)
    logf.flush()
    try: session.detach()
    except Exception: pass
    joined = '\n'.join(msgs)
    if '[★' in joined:
        log('[★] 命中 key!')
        break
log('=== 结束 ===')
logf.close()
