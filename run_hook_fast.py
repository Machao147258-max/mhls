# -*- coding: utf-8 -*-
# 快循环: 每轮 60s (稳定检查 20s + attach + hook + 触发 + 收集), 5 轮
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key5.js'
OUT = r'C:\Users\20751\tomdump\hook_fast_out.txt'
CYCLES = 5

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

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== 快循环 {time.strftime("%H:%M:%S")} ===')

for cyc in range(1, CYCLES + 1):
    log(f'--- 轮 {cyc} ---')
    pid = sh(['shell', 'pidof com.netease.tom'])
    if not pid.isdigit():
        sh(['shell', 'monkey -p com.netease.tom 1'])
        for _ in range(20):
            time.sleep(1)
            pid = sh(['shell', 'pidof com.netease.tom'])
            if pid.isdigit(): break
    log(f'  pid={pid or "无"}')
    if not pid.isdigit():
        continue
    # 稳定检查 10s (限时)
    dead = False
    t0 = time.time()
    while time.time() - t0 < 10:
        time.sleep(3)
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            dead = True
            break
    if dead:
        log('  稳定检查死亡, 下轮')
        continue
    log('  稳定 OK')
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
        log('  hook 加载')
    except Exception as e:
        log(f'  脚本失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    time.sleep(2)
    # 触发 + 收集 30s (整轮 ≤50s)
    sh(['shell', 'input keyevent 3'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    t_end = time.time() + 30
    last = 0
    while time.time() < t_end:
        time.sleep(5)
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
            log(f'  游戏死亡 (45s 观察内)')
            break
    log(f'  轮 {cyc} 结束, {len(msgs)} 条消息')
    try: session.detach()
    except Exception: pass
log('=== 结束 ===')
logf.close()
