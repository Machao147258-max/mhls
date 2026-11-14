# -*- coding: utf-8 -*-
# 最短路径: attach 当前游戏进程 + 装 hook (DELTA 一次性 + key 读点 + recv)
import frida, sys, time, threading

PORT = '127.0.0.1:45679'
HOOK_JS = r'''
'use strict';
var logf = null;
function log(s) {
    try {
        if (!logf) {
            logf = new File('/data/data/com.netease.tom/files/hooklog2.txt', 'a');
        }
        logf.write(s + '\n');
        logf.flush();
    } catch (e) {}
}
log('[+] hooked ' + Date.now());

// 1. 转译 x86 key 读点 (0x4f327b mov edx,[rsi] rsi=key指针) - 用 tcb 相对
// libtcb.so base 0x400060000000 (固定)
var KEY_OFF = 0x4f327b;

// 2. DELTA 一次性 (x86 转译代码)
var DELTA_OFFS = [0x4f3300, 0x4f335c, 0x4f32c0];
var hit_delta = false;

// 3. recv 追踪
var recv_ptr = Module.getExportByName('libc.so', 'recv');
if (recv_ptr) {
    Interceptor.attach(recv_ptr, {
        onEnter: function (args) {
            this.buf = args[1];
            this.n = args[2].toInt32();
        },
        onLeave: function (retval) {
            var n = retval.toInt32();
            if (n > 0 && n < 1000000) {
                try {
                    var b = Memory.readByteArray(this.buf, Math.min(n, 128));
                    var bytes = new Uint8Array(b);
                    var head = '';
                    for (var i = 0; i < Math.min(bytes.length, 16); i++) {
                        head += ('0' + bytes[i].toString(16)).slice(-2);
                    }
                    if (head.indexOf('58315635') === 0 || head.indexOf('1b4c7561') === 0) {
                        log('[recv] n=' + n + ' head=' + head);
                    }
                } catch (e) {}
            }
        }
    });
    log('[+] recv hooked');
}

// 4. 搜索 libtcb 里的 DELTA 指令并 hook
try {
    var tcb = Process.getModuleByName('libtcb.so');
    var base = tcb.base;
    log('[+] libtcb base=' + base + ' size=' + tcb.size);
    // 扫描 DELTA 常量 mov 0x9e3779b9
    var deltaBytes = [0xb9, 0x79, 0x37, 0x9e];
    var found = [];
    for (var off = 0; off < tcb.size - 4; off += 1) {
        try {
            var b = Memory.readByteArray(base.add(off), 4);
            var arr = new Uint8Array(b);
            if (arr[0] === deltaBytes[0] && arr[1] === deltaBytes[1] && arr[2] === deltaBytes[2] && arr[3] === deltaBytes[3]) {
                found.push(off);
            }
        } catch (e) { break; }
    }
    log('[+] DELTA x86 位置: ' + JSON.stringify(found));
    // hook 每个: 一次性
    found.forEach(function (off) {
        try {
            Interceptor.attach(base.add(off), {
                onEnter: function () {
                    if (!hit_delta) {
                        hit_delta = true;
                        log('[DELTA] FIRED @' + off.toString(16) + ' ' + Date.now());
                        // 抓寄存器上下文
                        try {
                            var ctx = this.context;
                            var regs = {};
                            ['eax', 'ebx', 'ecx', 'edx', 'esi', 'edi', 'ebp', 'esp'].forEach(function (r) {
                                if (ctx[r]) regs[r] = ctx[r].toString(16);
                            });
                            log('[DELTA] regs=' + JSON.stringify(regs));
                        } catch (e2) { log('[DELTA] ctx err ' + e2); }
                    }
                }
            });
        } catch (e3) {}
    });
} catch (e) {
    log('[!] libtcb err: ' + e);
}

// 5. key 读点 hook: 0x4f327b (x86) 即 tcb+0x4f327b
try {
    var tcb2 = Process.getModuleByName('libtcb.so');
    Interceptor.attach(tcb2.base.add(0x4f327b), {
        onEnter: function () {
            try {
                var ctx = this.context;
                var rsi = ctx.rsi;
                log('[KEYPOINT] 0x4f327b rsi=' + rsi);
                if (rsi && !rsi.isNull()) {
                    var b = Memory.readByteArray(rsi, 16);
                    var arr = new Uint8Array(b);
                    var hex = '';
                    for (var i = 0; i < 16; i++) hex += ('0' + arr[i].toString(16)).slice(-2);
                    log('[KEYPOINT] key16=' + hex);
                    var asc = '';
                    for (var i = 0; i < 16; i++) asc += (arr[i] >= 32 && arr[i] < 127) ? String.fromCharCode(arr[i]) : '.';
                    log('[KEYPOINT] ascii=' + asc);
                }
            } catch (e) { log('[KEYPOINT] err ' + e); }
        }
    });
    log('[+] keypoint hooked');
} catch (e) {
    log('[!] keypoint err: ' + e);
}

// 6. 防自杀: hook raise/abort/exit
['raise', 'abort', '_exit', 'exit', 'pthread_kill', 'tgkill', 'kill'].forEach(function (f) {
    try {
        var p = Module.getExportByName('libc.so', f);
        if (p) {
            Interceptor.replace(p, new NativeCallback(function (a, b) {
                log('[KILL-ATTEMPT] ' + f + '(' + a + ',' + b + ') BLOCKED');
                return 0;
            }, 'int', ['int', 'int']));
        }
    } catch (e2) {}
});
log('[+] all hooks done');
'''

def main():
    dev = frida.get_device_manager().add_remote_device(PORT)
    pid = int(sys.argv[1]) if len(sys.argv) > 1 else None
    if pid:
        session = dev.attach(pid)
    else:
        # 找游戏进程
        procs = dev.enumerate_processes()
        pid = None
        for p in procs:
            if p.name == 'com.netease.tom':
                pid = p.pid
                break
        if not pid:
            print('游戏进程未找到')
            return
        session = dev.attach(pid)
    print('attached', pid)
    script = session.create_script(HOOK_JS)
    script.on('message', lambda m, d: print('MSG:', m))
    script.load()
    print('hooks installed, waiting...')
    # 保持 5 分钟
    time.sleep(300)

if __name__ == '__main__':
    main()
