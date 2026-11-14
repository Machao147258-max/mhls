# -*- coding: utf-8 -*-
# x86 转译版 key 读点 hook: 0x4f327b mov edx,[rsi] (rsi=key 指针)
# 直接 attach 当前进程, 记录 rsi 指向的 16 字节
import frida, sys, time

HOOK_JS = r"""
'use strict';
// x86 转译缓存 key 加载点: libtcb base 0x400060000000 + 0x4f327b? 实际转译段 0x400060174000+0x4f327b
// 用内存扫描兜底: hook 点 = 0x400060174000 + (0x4f335c - 0x40) 区域
var logfile = '/data/data/com.netease.tom/files/keyhook2.txt';
function log(s) {
    try {
        var f = new File(logfile, 'a');
        f.write(s + '\n');
        f.close();
    } catch (e) {}
}
log('[+] keyhook load ' + Date.now());

// 尝试多个候选点 (x86 转译 key mov edx,[rsi])
var candidates = [
    0x400060174000 + 0x4f327b,   // 已知 mov edx,[rsi]
    0x400060174000 + 0x4f335c,   // DELTA 使用点
];
for (var i = 0; i < candidates.length; i++) {
    var addr = candidates[i];
    try {
        // 验证这是可执行内存
        var m = Process.findRangeByAddress(ptr(addr));
        if (!m) { log('[!] 候选不可达 ' + addr.toString(16)); continue; }
        // 读该处指令 (验证 0x8b = mov)
        var b = m.base.add(addr.sub(m.base)).readByteArray(8);
        log('[+] 候选 ' + addr.toString(16) + ' 指令: ' + b);
        Interceptor.attach(ptr(addr), {
            onEnter: function (args) {
                try {
                    var rsi = this.context.rsi;
                    if (rsi) {
                        var key = rsi.readByteArray(16);
                        log('[★KEY] rsi=' + rsi + ' key=' + key);
                    }
                } catch (e) { log('[!] read err ' + e); }
            }
        });
        log('[+] hooked ' + addr.toString(16));
    } catch (e) {
        log('[!] hook err ' + addr.toString(16) + ' ' + e);
    }
}
log('[+] done');
"""

def main():
    dev = frida.get_device_manager().add_remote_device('127.0.0.1:45679')
    pid = int(sys.argv[1])
    print('attach %d...' % pid)
    session = dev.attach(pid)
    print('attached!')
    script = session.create_script(HOOK_JS)
    script.on('message', lambda m, d: print('[msg]', m))
    script.load()
    print('hook loaded, 观察 180s (Ctrl+C 退出)')
    time.sleep(180)

if __name__ == '__main__':
    main()