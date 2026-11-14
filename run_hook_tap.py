# -*- coding: utf-8 -*-
# attach 已运行游戏 + hook_key5 + adb 点击触发切场景 → 抓解密
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key5.js'
OUT = r'C:\Users\20751\tomdump\hook_tap_out.txt'

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

# 确保游戏运行并进入主界面
pid = sh(['shell', 'pidof com.netease.tom'])
if not pid.isdigit():
    log('[-] 游戏未运行, 启动...')
    sh(['shell', 'monkey -p com.netease.tom 1'])
    for _ in range(60):
        time.sleep(1)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit():
            break
    if not pid.isdigit():
        log('[-] 启动失败')
        raise SystemExit
log(f'[+] PID={pid}')
# 等 so 加载 + 进入主界面
for _ in range(90):
    time.sleep(2)
    so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
    if so.isdigit() and int(so) > 0:
        break
log('[+] 等待游戏进入主界面 30s...')
time.sleep(30)

dev = frida.get_device_manager().add_remote_device('127.0.0.1:31337')
msgs = []
def on_message(msg, data):
    t = msg.get('type')
    if t == 'send': msgs.append(str(msg['payload']))
    elif t == 'log': msgs.append(str(msg.get('payload', '')))
    elif t == 'error': msgs.append('ERR: ' + str(msg.get('stack', ''))[:300])
try:
    session = dev.attach(int(pid))
    log('[+] attach OK')
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', on_message)
    script.load()
    log('[+] hook 已装')
except Exception as e:
    log(f'[-] 失败: {e}')
    raise SystemExit

# 点击触发: 1080x1920, 常见主界面按钮
taps = [
    (540, 900, '中央'), (540, 1200, '中央偏下'), (540, 1500, '下部'),
    (540, 600, '中上'), (900, 1700, '右下'), (180, 1700, '左下'),
    (540, 960, '正中央'), (270, 480, '左上'),
]
for i in range(2):
    for x, y, name in taps:
        sh(['shell', f'input tap {x} {y}'])
        time.sleep(6)
        joined = '\n'.join(msgs)
        log(f'--- tap {name} ({x},{y}) 后消息 {len(msgs)} 条 ---')
        if '[★' in joined:
            log('[★] 命中 key!!')
            break
        # 打印新消息
        for m in msgs[-5:]:
            log('  |', m)
    if '[★' in '\n'.join(msgs):
        break

for m in msgs:
    log('FINAL |', m)
log('=== 结束 ===')
logf.close()
try: session.detach()
except Exception: pass
