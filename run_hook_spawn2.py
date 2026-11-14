# -*- coding: utf-8 -*-
# spawn + hook_key8 (文件日志): 启动早期 hook, 抓启动解密
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_key10.js'
OUT = r'C:\Users\20751\tomdump\hook_spawn2_out.txt'
CYCLES = 3
WAIT = 240

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

def read_log():
    return sh(['shell', 'su -c "cat /data/data/com.netease.tom/files/hooklog.txt 2>/dev/null"'])

dev = frida.get_device_manager().add_remote_device('127.0.0.1:45678')
log(f'=== spawn+文件日志 {time.strftime("%H:%M:%S")} ===')

for cyc in range(1, CYCLES + 1):
    log(f'--- 周期 {cyc} ---')
    sh(['shell', 'su -c "rm -f /data/data/com.netease.tom/files/hooklog.txt"'])
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    try:
        pid = dev.spawn('com.netease.tom')
        log(f'[+] spawn {pid}')
    except Exception as e:
        log(f'[-] spawn 失败: {e}')
        continue
    session = None
    try:
        session = dev.attach(pid)
        script = session.create_script(open(JS, encoding='utf-8').read())
        script.on('message', lambda m, d: None)
        script.load()
        log('[+] 脚本加载, resume')
        dev.resume(pid)
    except Exception as e:
        log(f'[-] 注入失败: {e}')
        try: dev.resume(pid)
        except Exception: pass
        continue
    # 轮询文件日志
    seen = set()
    t_end = time.time() + WAIT
    got = False
    while time.time() < t_end:
        time.sleep(3)
        hl = read_log()
        for line in hl.splitlines():
            if line not in seen:
                seen.add(line)
                log('  |', line)
                if '[★' in line:
                    got = True
        if got:
            log('[★] 命中!')
            break
    try: session.detach()
    except Exception: pass
    if got:
        break
log('=== 结束 ===')
logf.close()
