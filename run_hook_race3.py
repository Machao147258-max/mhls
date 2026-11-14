# -*- coding: utf-8 -*-
# 抢时机驱动 v2: 文件日志版 (hook_key8), 驱动轮询读 hooklog.txt
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key8.js'
OUT = r'C:\Users\20751\tomdump\hook_race3_out.txt'
ROUNDS = 5
WAIT = 140

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

def read_hooklog():
    r = sh(['shell', 'su -c "cat /data/data/com.netease.tom/files/hooklog.txt 2>/dev/null"'])
    return r

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== 抢时机 v2 {time.strftime("%H:%M:%S")} ===')

for rnd in range(1, ROUNDS + 1):
    log(f'--- 轮 {rnd} ---')
    sh(['shell', 'su -c "rm -f /data/data/com.netease.tom/files/hooklog.txt"'])
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    sh(['shell', 'monkey -p com.netease.tom 1'])
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
    log(f'[+] PID={pid} 出现 {time.time()-t0:.1f}s')
    try:
        session = dev.attach(int(pid))
        log(f'[+] attach {time.time()-t0:.1f}s')
    except Exception as e:
        log(f'[-] attach 失败: {e}')
        continue
    script = session.create_script(open(JS, encoding='utf-8').read())
    script.on('message', lambda m, d: None)
    try:
        script.load()
        log(f'[+] 脚本加载 {time.time()-t0:.1f}s')
    except Exception as e:
        log(f'[-] 脚本失败: {e}')
        try: session.detach()
        except Exception: pass
        continue
    # 轮询读 hooklog
    seen = set()
    t1 = time.time()
    got_key = False
    while time.time() - t1 < WAIT:
        time.sleep(3)
        hl = read_hooklog()
        for line in hl.splitlines():
            if line not in seen:
                seen.add(line)
                log('  |', line)
                if '★' in line or ('[★' in line):
                    got_key = True
        try:
            script.post({})
        except Exception:
            log('[-] 脚本死亡')
            break
        if got_key:
            log('[★] 命中!')
            break
    try: session.detach()
    except Exception: pass
    if got_key:
        break
log('=== 结束 ===')
logf.close()
