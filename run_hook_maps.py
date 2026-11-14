# -*- coding: utf-8 -*-
# spawn + hook_maps (过滤 maps 反检测): 3 轮 × 180s
import frida, time, subprocess

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
JS = r'C:\Users\20751\Desktop\猫和老鼠\hook_maps.js'
OUT = r'C:\Users\20751\tomdump\hook_maps_out.txt'
CYCLES = 3
WAIT = 180

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
log(f'=== spawn+maps过滤 {time.strftime("%H:%M:%S")} ===')
for cyc in range(1, CYCLES + 1):
    log(f'--- 轮 {cyc} ---')
    sh(['shell', 'su -c "rm -f /data/data/com.netease.tom/files/hooklog.txt"'])
    sh(['shell', 'am force-stop com.netease.tom'])
    time.sleep(2)
    try:
        pid = dev.spawn('com.netease.tom')
        log(f'[+] spawn {pid}')
    except Exception as e:
        log(f'[-] spawn 失败: {e}')
        continue
    try:
        session = dev.attach(pid)
        script = session.create_script(open(JS, encoding='utf-8').read())
        script.on('message', lambda m, d: None)
        script.load()
        dev.resume(pid)
        log('[+] resume')
    except Exception as e:
        log(f'[-] 注入失败: {e}')
        try: dev.resume(pid)
        except Exception: pass
        continue
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
                if '[★' in line or '[防自杀]' in line:
                    got = True
        if got:
            log('[!] 关键事件! 继续观察...')
            got = False
        if '[★decwrap]' in hl:
            log('[★★★] 抓到 key!!')
            break
        # 游戏死了?
        if not sh(['shell', 'pidof com.netease.tom']).isdigit() and '等待解密' in hl:
            log('[-] 游戏死亡')
            break
    try: session.detach()
    except Exception: pass
log('=== 结束 ===')
logf.close()
