# -*- coding: utf-8 -*-
# 后台 hook 观察: attach + hook_key5 + 切前后台触发 + 180s 收集, 详细落盘
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key5.js'
OUT = r'C:\Users\20751\tomdump\hook_bg_out.txt'

def sh(args, t=15):
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

# 观察游戏
pid = sh(['shell', 'pidof com.netease.tom'])
log(f'[1] 游戏 PID={pid or "无"}')
if not pid.isdigit():
    log('[1!] 未运行, 启动...')
    sh(['shell', 'monkey -p com.netease.tom 1'])
    for _ in range(30):
        time.sleep(2)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit(): break
log(f'[2] 确认 PID={pid}')
# 复检稳定 20s
t0 = time.time()
while time.time() - t0 < 20:
    time.sleep(5)
    if not sh(['shell', 'pidof com.netease.tom']).isdigit():
        log('[3!] 游戏死亡, 结束')
        logf.close(); raise SystemExit
log('[3] 20s 复检稳定')

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
msgs = []
try:
    session = dev.attach(int(pid))
    log('[4] attach OK')
except Exception as e:
    log(f'[4!] attach 失败: {e}')
    logf.close(); raise SystemExit

def on_message(msg, data):
    t = msg.get('type')
    line = str(msg.get('payload', msg.get('stack', '')))[:300]
    if t in ('send', 'log'):
        msgs.append(line)
        log('[hook]', line)
    elif t == 'error':
        log('[err]', line)

script = session.create_script(open(JS, encoding='utf-8').read())
script.on('message', on_message)
try:
    script.load()
    log('[5] hook 已加载')
except Exception as e:
    log(f'[5!] 失败: {e}')
    logf.close(); raise SystemExit
time.sleep(2)
log(f'[6] 安装输出 {len(msgs)} 条')
for m in msgs[:15]:
    log('   |', m)

# 触发: 切后台回前台 + 等待自然加载
log('[7] 切后台回前台触发...')
sh(['shell', 'input keyevent 3'])
time.sleep(6)
sh(['shell', 'monkey -p com.netease.tom 1'])
time.sleep(6)
log('[8] 触发完成, 观察 180s (自然加载)...')
last = len(msgs)
t_end = time.time() + 180
while time.time() < t_end:
    time.sleep(10)
    if len(msgs) > last:
        log(f'[t+{180-(t_end-time.time()):.0f}s] 新消息 {len(msgs)-last} 条')
        for m in msgs[last:]:
            log('   |', m)
        last = len(msgs)
    if '[★' in '\n'.join(msgs):
        log('[★] 命中 key!!')
        break
    if not sh(['shell', 'pidof com.netease.tom']).isdigit():
        log('[9!] 游戏死亡')
        break
log(f'[10] 结束, 共 {len(msgs)} 条')
logf.close()
try: session.detach()
except Exception: pass
