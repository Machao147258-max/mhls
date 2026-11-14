# -*- coding: utf-8 -*-
# 稳定后 attach: 启动循环 → 存活 60s → attach + hook_key5 → 点击触发 → 抓解密
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key9.js'
OUT = r'C:\Users\20751\tomdump\hook_stable_out.txt'
MAX_START = 6
HOOK_TIME = 300

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
log(f'=== 稳定 attach {time.strftime("%H:%M:%S")} ===')

pid = None
for attempt in range(1, MAX_START + 1):
    log(f'--- 启动尝试 {attempt} ---')
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    t0 = time.time()
    while time.time() - t0 < 45:
        out = sh(['shell', 'pidof com.netease.tom'])
        if out.isdigit():
            pid = out
            break
        time.sleep(0.5)
    if not pid:
        continue
    # 等 60 秒存活检查 (进主界面)
    alive = True
    t0 = time.time()
    while time.time() - t0 < 60:
        time.sleep(5)
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            alive = False
            log(f'  第 {time.time()-t0:.0f}s 死亡')
            break
    if alive:
        log(f'[+] PID={pid} 稳定存活 60s+')
        break
    pid = None

if not pid:
    log('[-] 多次启动均未稳定')
    logf.close()
    raise SystemExit

# attach + hook
msgs = []
def on_message(msg, data):
    t = msg.get('type')
    if t == 'send': msgs.append(str(msg['payload']))
    elif t == 'log': msgs.append(str(msg.get('payload', '')))
    elif t == 'error': msgs.append('ERR: ' + str(msg.get('stack', ''))[:200])
try:
    session = dev.attach(int(pid))
    log('[+] attach OK')
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', on_message)
    script.load()
    log('[+] hook 已装')
except Exception as e:
    log(f'[-] attach 失败: {e}')
    logf.close()
    raise SystemExit

# 触发: 2 秒疯狂点击 + 快速收集 (attach 后窗口有限)
taps = [(540, 960), (540, 1200), (540, 1500), (540, 600), (900, 1700), (540, 900),
        (270, 480), (810, 480), (540, 300), (540, 1700), (270, 1500), (810, 1500),
        (540, 100), (900, 300), (180, 900), (900, 900), (540, 1400), (540, 700)]
t_end = time.time() + HOOK_TIME
tap_i = 0
last_out = 0
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
        break
    if not sh(['shell', 'pidof com.netease.tom']).isdigit():
        log('[-] 游戏死亡')
        break

for m in msgs:
    log('FINAL |', m)
log('=== 结束 ===')
logf.close()
try: session.detach()
except Exception: pass
