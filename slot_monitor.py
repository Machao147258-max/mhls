# -*- coding: utf-8 -*-
# 最短路径: 监控游戏进程 → so 加载 → 解密后 → 直接读内存槽(0xff6cc50)拿单例 → key
import subprocess, time, sys, os

ADB = r'D:\MuMuPlayer\nx_main\adb.exe'
OUT = r'C:\Users\20751\tomdump\slot_read'
os.makedirs(OUT, exist_ok=True)

def sh(args, t=20):
    try:
        r = subprocess.run([ADB, '-s', '127.0.0.1:7555'] + args, capture_output=True, timeout=t)
        return (r.stdout.decode('utf-8', 'replace') + r.stderr.decode('utf-8', 'replace')).strip()
    except Exception as e:
        return ''

def get_pid():
    p = sh(['shell', 'su -c pidof com.netease.tom']).strip()
    for tok in p.split():
        if tok.isdigit():
            return tok
    return None

def get_cocos_base(pid):
    m = sh(['shell', 'su -c cat /proc/%s/maps' % pid])
    for line in m.splitlines():
        if 'libcocos2dlua' in line and 'r--p' in line:
            return line.split('-')[0]
    return None

def read_mem(pid, addr_hex, n):
    """读进程内存 (dd skip=addr count=n)"""
    r = sh(['shell', 'su -c "dd if=/proc/%s/mem bs=1 skip=$((0x%s)) count=%d 2>/dev/null | xxd -p"' % (pid, addr_hex, n)], t=30)
    return r.replace('\n', '').strip()

log = open(os.path.join(OUT, 'monitor.log'), 'w')
def logw(s):
    print(s)
    log.write(s + '\n')
    log.flush()

pid0 = get_pid()
logw('初始 pid: %s' % pid0)
start = time.time()
seen_pids = {}
while time.time() - start < 600:
    pid = get_pid()
    if pid:
        if pid not in seen_pids:
            seen_pids[pid] = time.time()
            logw('[%ds] pid %s (新进程)' % (int(time.time() - start), pid))
        base = get_cocos_base(pid)
        if base:
            # 等解密 (so 加载后 60-120s, launcher 解密窗口)
            t_loaded = time.time()
            logw('[%ds] libcocos2dlua 加载! base=%s (pid %s) 等解密窗口 90s...' % (int(time.time() - start), base, pid))
            time.sleep(90)
            # 读槽: base + 0xff6cc50
            slot = '%x' % (int(base, 16) + 0xff6cc50)
            v = read_mem(pid, slot, 8)
            logw('[%ds] 槽(%s) 值: %s' % (int(time.time() - start), slot, v))
            if v and v != '00' * 8:
                # 单例指针
                ptr = int(v, 16)
                logw('单例指针: %#x' % ptr)
                # 读单例前 0x60 (key 可能在 +0 / +0x10 / 附近)
                for off in (0x0, 0x8, 0x10, 0x18, 0x20, 0x28, 0x30):
                    av = read_mem(pid, '%x' % (ptr + off), 16)
                    logw('  单例+%#x: %s' % (off, av))
                # 也读全槽区 (槽附近可能有 key)
                for off in (0xff6cbf0, 0xff6cc00, 0xff6cc10, 0xff6cc20, 0xff6cc30, 0xff6cc40, 0xff6cc50, 0xff6cc60, 0xff6cc70, 0xff6cc80):
                    av = read_mem(pid, '%x' % (int(base, 16) + off), 16)
                    logw('  so+%#x: %s' % (off, av))
                logw('DONE')
                sys.exit(0)
            else:
                logw('[%ds] 槽为空(解密可能未发生), 继续等...' % int(time.time() - start))
                # 再等 60s 重试
                time.sleep(60)
        else:
            # so 未加载: 检查进程还活着?
            if int(time.time() - start) % 60 < 12:
                logw('[%ds] 等待 so 加载 (pid=%s)...' % (int(time.time() - start), pid))
    else:
        logw('[%ds] 游戏进程不存在! 等待...' % int(time.time() - start))
    time.sleep(10)
logw('超时结束')
