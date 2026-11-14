// tb_guard: 反处决护盾 —— 接管 watchdog 的杀进程路径(kill/tgkill/pthread_kill/raise/abort/exit/_exit)
// 用法: frida -H 127.0.0.1:31337 -p <PID> -l tb_guard.js   (可长时间挂着,与抓取脚本同 session 混合使用)
function log(m) { console.log(m); }

// 可疑 watchdog 线程名(按之前观察到的)
var SUS = /trace|stack|guard|watch|sec|anti|detect|dTi/i;
var FATAL = { 4: 1, 5: 1, 6: 1, 7: 1, 8: 1, 9: 1, 11: 1 };  // ILL TRAP ABRT BUS FPE KILL SEGV
var myPid = -1;
var suppressed = 0;

function getTidName(tid) {
    try {
        var t = Process.enumerateThreads().find(function (x) { return x.id === tid; });
        return t ? t.name : '?';
    } catch (e) { return '?'; }
}

function isSuspicious(tid) {
    var n = getTidName(tid);
    return SUS.test(n) || /^\w{1,3}$/.test(n);   // 短名(如 dTi)也视为可疑
}

function replaceFn(addr, impl) {
    try {
        Interceptor.replace(addr, new NativeCallback(impl, 'void', []));
        return true;
    } catch (e) { return false; }
}

setTimeout(function () {
    myPid = Process.id;
    log('[*] tb_guard attach ok, pid=' + myPid);
    var libc = Process.findModuleByName('libc.so');
    if (!libc) { log('[-] libc 未找到'); return; }

    // 每个 kill 类函数: 若目标是自身进程且信号致命 → 吞掉; 否则转发原实现
    function mkKillHandler(orig, kind) {
        return function (a, b, c) {
            var pid = a, sig = b;
            var tid = Process.getCurrentThreadId();
            if (kind === 'tgkill') { pid = a; sig = c; }
            if (kind === 'pthread_kill') { pid = myPid; sig = b; }
            if (kind === 'raise') { pid = myPid; sig = a; }
            var targetSelf = (pid === myPid || pid === 0);
            if (targetSelf && FATAL[sig]) {
                suppressed++;
                log('[guard] 吞掉信号 ' + sig + ' 来自 tid=' + tid + ' (' + getTidName(tid) + ') 总计' + suppressed);
                return 0;
            }
            var f = new NativeFunction(orig, 'int', ['int', 'int', 'int']);
            try { return kind === 'tgkill' ? f(a, b, c) : (kind === 'pthread_kill' ? f(a, b) : f(pid, sig)); }
            catch (e) { return 0; }
        };
    }

    [['kill', 'kill'], ['tgkill', 'tgkill'], ['pthread_kill', 'pthread_kill'], ['raise', 'raise']].forEach(function (p) {
        try {
            var addr = Module.findGlobalExportByName(p[0]);
            if (!addr) return;
            var orig = new NativeFunction(addr, 'int', ['int', 'int', 'int']);
            Interceptor.replace(addr, new NativeCallback(mkKillHandler(orig, p[1]), 'int', ['int', 'int', 'int']));
            log('[+] 接管 ' + p[0]);
        } catch (e) { log('[-] ' + p[0] + ' 接管失败: ' + e); }
    });

    // abort / exit / _exit: 可疑线程调用时拦截(不转发, 线程悬挂在自旋里)
    [['abort', 'void', []], ['exit', 'void', ['int']], ['_exit', 'void', ['int']]].forEach(function (p) {
        try {
            var addr = Module.findGlobalExportByName(p[0]);
            if (!addr) return;
            var orig = new NativeFunction(addr, 'void', ['int']);
            Interceptor.replace(addr, new NativeCallback(function (code) {
                var tid = Process.getCurrentThreadId();
                if (isSuspicious(tid)) {
                    suppressed++;
                    log('[guard] 拦截 ' + p[0] + ' 来自 tid=' + tid + ' (' + getTidName(tid) + ') 总计' + suppressed);
                    while (true) { Thread.sleep(1); }   // 挂住调用线程,不退出进程
                }
                try { orig(code); } catch (e) {}
            }, p[1], p[2]));
            log('[+] 接管 ' + p[0]);
        } catch (e) { log('[-] ' + p[0] + ' 接管失败: ' + e); }
    });

    log('[*] tb_guard 就绪,可进入游戏大厅');
    setInterval(function () { }, 1000);
}, 2000);