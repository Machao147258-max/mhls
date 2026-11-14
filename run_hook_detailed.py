# -*- coding: utf-8 -*-
# 稳定确认 → attach → hook → 疯狂点击触发 → 抓解密, 详细日志
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key5.js'
OUT = r'C:\Users\20751\tomdump\hook_detailed_out.txt'

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

# [1] 确认游戏稳定
pid = sh(['shell', 'pidof com.netease.tom'])
log(f'[1] 游戏 PID={pid or "无"}')
if not pid.isdigit():
    log('[1!] 游戏未运行, 结束')
    logf.close(); raise SystemExit
so = sh(['shell', f'cat /proc/{pid}/maps 2>/dev/null | grep -c cocos'])
log(f'[2] so 段数={so}')
fg = sh(['shell', 'dumpsys activity activities | grep topResumedActivity | head -1'])[:100]
log(f'[3] 前台={fg}')
t0 = time.time()
stable = True
while time.time() - t0 < 30:
    time.sleep(5)
    if not sh(['shell', 'pidof com.netease.tom']).isdigit():
        stable = False
        log(f'[4!] 第 {time.time()-t0:.0f}s 游戏死亡!')
        break
log(f'[4] 30s 复检: {"稳定" if stable else "死亡"}')

# [5] attach
log('[5] 尝试 attach...')
dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
msgs = []
try:
    session = dev.attach(int(pid))
    log('[5+] attach 成功')
except Exception as e:
    log(f'[5!] attach 失败: {e}')
    logf.close(); raise SystemExit

def on_message(msg, data):
    t = msg.get('type')
    if t == 'send': msgs.append(str(msg['payload']))
    elif t == 'log': msgs.append(str(msg.get('payload', '')))
    elif t == 'error': msgs.append('ERR: ' + str(msg.get('stack', ''))[:200])

script = session.create_script(open(JS, encoding='utf-8').read())
script.on('message', on_message)
try:
    script.load()
    log('[6] hook 脚本已加载')
except Exception as e:
    log(f'[6!] 脚本失败: {e}')
    logf.close(); raise SystemExit
time.sleep(2)
log(f'[7] hook 安装输出 ({len(msgs)} 条):')
for m in msgs[:20]:
    log('     |', m)
log('[8] 开始疯狂点击触发 (每 2 秒, 最多 90 秒)...')
taps = [(540,960),(540,1200),(540,1500),(540,600),(900,1700),(540,900),
        (270,480),(810,480),(540,300),(540,1700),(270,1500),(810,1500),
        (540,100),(900,300),(180,900),(900,900),(540,1400),(540,700)]
tap_i = 0
last_out = 0
t_end = time.time() + 90
while time.time() < t_end:
    x, y = taps[tap_i % len(taps)]
    tap_i += 1
    sh(['shell', f'input tap {x} {y}'])
    time.sleep(2)
    if len(msgs) > last_out:
        for m in msgs[last_out:]:
            log(f'[{time.time()-t_end+90:.0f}s] hook: {m}')
        last_out = len(msgs)
    if '[★' in '\n'.join(msgs):
        log('[★] 命中 key!!')
        break
    if not sh(['shell', 'pidof com.netease.tom']).isdigit():
        log(f'[9!] 游戏死亡 (点击 {tap_i} 次, {time.time()-t0:.0f}s)')
        break
else:
    log('[9] 90 秒窗口结束, 游戏仍存活')
log(f'[10] 结束, 共 {tap_i} 次点击, {len(msgs)} 条 hook 消息')
for m in msgs:
    log('FINAL |', m)
logf.close()
try: session.detach()
except Exception: pass
