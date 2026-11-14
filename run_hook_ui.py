# -*- coding: utf-8 -*-
# 启动循环 → 稳定 → attach → UI 点击触发加载 → 抓解密
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key5.js'
OUT = r'C:\Users\20751\tomdump\hook_ui_out.txt'

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

def ui_buttons():
    sh(['shell', 'uiautomator dump /data/local/tmp/ui.xml'])
    r = sh(['shell', 'su -c "cat /data/local/tmp/ui.xml 2>/dev/null"'])
    import re
    out = []
    for m in re.finditer(r'text="([^"]{1,24})"[^>]*?bounds="\[(\d+),(\d+)\]\[(\d+),(\d+)\]"', r):
        t = m.group(1)
        x1, y1, x2, y2 = map(int, m.group(2, 3, 4, 5))
        if t.strip():
            out.append((t, (x1 + x2) // 2, (y1 + y2) // 2))
    return out

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== UI 触发 {time.strftime("%H:%M:%S")} ===')

for rnd in range(1, 6):
    log(f'--- 轮 {rnd} ---')
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
    pid = None
    for _ in range(40):
        time.sleep(1)
        pid = sh(['shell', 'pidof com.netease.tom'])
        if pid.isdigit(): break
    if not pid.isdigit():
        log('  启动失败'); continue
    # 稳定 50s
    t0 = time.time()
    dead = False
    while time.time() - t0 < 50:
        time.sleep(5)
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            dead = True; break
    if dead:
        log('  未稳定'); continue
    log(f'  稳定 PID={pid}')
    # attach
    try:
        session = dev.attach(int(pid))
        log('  attach OK')
    except Exception as e:
        log(f'  attach 失败: {e}'); continue
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
    # UI 点击: 依次点可见按钮 (避开底部导航)
    last = 0
    t_end = time.time() + 75
    while time.time() < t_end:
        btns = ui_buttons()
        targets = [b for b in btns if b[1] > 200 and b[1] < 1840 and b[2] > 150 and b[2] < 1700]
        log(f'  按钮 {len(targets)} 个: {[b[0] for b in targets[:6]]}')
        for name, x, y in targets[:4]:
            sh(['shell', f'input tap {x} {y}'])
            time.sleep(3)
            if len(msgs) > last:
                for m in msgs[last:]:
                    log('    |', m)
                last = len(msgs)
            if '[★' in '\n'.join(msgs):
                log('  [★] 命中!')
                for m in msgs: log('    FINAL |', m)
                logf.close()
                raise SystemExit
            if not sh(['shell', 'pidof com.netease.tom']).isdigit():
                log('  游戏死亡'); break
        if not sh(['shell', 'pidof com.netease.tom']).isdigit():
            break
    log(f'  轮 {rnd} 结束 {len(msgs)} 条')
    try: session.detach()
    except Exception: pass
log('=== 结束 ===')
logf.close()
