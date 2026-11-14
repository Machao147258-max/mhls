# -*- coding: utf-8 -*-
# 自主 hook 驱动: attach → 抓 XXTEAUtil 单例 + 解密调用 → 无果则重启游戏触发 → 循环
# 输出: hook_run_out.txt (实时追加)
import frida, sys, time, subprocess, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
DEV = '127.0.0.1:7555'
JS_PATH = r'C:\Users\20751\Desktop\猫和老鼠\hook_key3.js'
OUT = r'C:\Users\20751\tomdump\hook_run_out.txt'
ROUNDS = 6
WAIT_AFTER_ATTACH = 150  # 每轮 attach 后等待秒数

logf = open(OUT, 'a', encoding='utf-8')
def log(*a):
    s = ' '.join(str(x) for x in a)
    print(s, flush=True)
    logf.write(s + '\n')
    logf.flush()

def sh(args, t=40):
    try:
        r = subprocess.run([ADB, '-s', DEV] + args, capture_output=True, timeout=t)
        return r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')
    except Exception as e:
        return f'ERR {e}'

def get_pid():
    out = sh(['shell', 'pidof com.netease.tom']).strip()
    return out if out and out.isdigit() else None

def so_loaded(pid):
    out = sh(['shell', f'cat /proc/{pid}/maps | grep -c libcocos2dlua']).strip()
    return out and int(out) > 0

class Collector:
    def __init__(self):
        self.msgs = []
    def on_message(self, msg, data):
        if msg.get('type') == 'send':
            self.msgs.append(str(msg['payload']))
            log('[send]', msg['payload'])
        elif msg.get('type') == 'error':
            log('[error]', msg.get('stack') or msg.get('description'))
        else:
            log('[msg]', msg)

dev = frida.get_device_manager().add_remote_device('127.0.0.1:31337')
log(f'=== 会话开始 {time.strftime("%H:%M:%S")} frida ok ===')

for rnd in range(1, ROUNDS + 1):
    log(f'\n--- 第 {rnd} 轮 ---')
    # 1) 重启游戏
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    session = None
    pid = None
    # 2) 尝试 spawn 模式 (早注入)
    try:
        pid = dev.spawn('com.netease.tom')
        log(f'[+] spawn PID={pid}')
    except Exception as e:
        log(f'[-] spawn 失败: {e}, 用 monkey 启动')
        sh(['shell', 'monkey -p com.netease.tom 1'])
        for _ in range(30):
            pid = get_pid()
            if pid: break
            time.sleep(1)
        if not pid:
            log('[-] 游戏未启动')
            continue
        log(f'[+] PID={pid}')
        for _ in range(60):
            if so_loaded(pid): break
            time.sleep(1)
        log(f'[+] so 加载: {so_loaded(pid)}')
    # 3) attach
    try:
        session = dev.attach(int(pid))
        log('[+] attach 成功')
    except Exception as e:
        log(f'[-] attach 失败: {e}')
        try:
            dev.resume(int(pid))
        except Exception:
            pass
        continue
    # 4) spawn 模式 resume
    try:
        dev.resume(int(pid))
        log('[+] resume')
    except Exception:
        pass
    coll = Collector()
    script = session.create_script(open(JS_PATH, encoding='utf-8').read())
    script.on('message', coll.on_message)
    try:
        script.load()
        log('[+] 脚本已加载')
    except Exception as e:
        log(f'[-] 脚本加载失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    # 5) 等待收集
    t0 = time.time()
    while time.time() - t0 < WAIT_AFTER_ATTACH:
        time.sleep(5)
        alive = True
        try:
            script.post({})  # 探活
        except Exception:
            alive = False
        if not alive:
            log('[-] 脚本已死(可能闪退)')
            break
        # 检查是否已抓到 key
        joined = '\n'.join(coll.msgs)
        if '[★] KEYS=' in joined and '[]' not in joined.split('[★] KEYS=')[1][:40]:
            log('[★] 已抓到 KEYS, 提前结束本轮等待')
            break
    try: session.detach()
    except Exception: pass
    # 6) 判断结果
    joined = '\n'.join(coll.msgs)
    if '[DEC]' in joined or ('[★] KEYS=' in joined and '[]' not in joined.split('[★] KEYS=')[1][:40]):
        log('[★] 本轮有 key 结果! 保存完成')
        break
    log('[-] 本轮无 key, 下一轮')

log('=== 会话结束 ===')
logf.close()
