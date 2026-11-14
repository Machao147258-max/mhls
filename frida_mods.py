# -*- coding: utf-8 -*-
"""frida 附加 com.netease.tom，枚举加载的 so 模块，确认 SSL 栈"""
import frida, sys, time

dev = frida.get_device_manager().add_remote_device("127.0.0.1:27042")

script_src = r"""
(function () {
    var mods = Process.enumerateModules();
    var interesting = [];
    for (var i = 0; i < mods.length; i++) {
        var m = mods[i];
        var n = m.name.toLowerCase();
        if (n.indexOf('ssl') !== -1 || n.indexOf('crypto') !== -1 || n.indexOf('cocos') !== -1 ||
            n.indexOf('audio') !== -1 || n.indexOf('sec') !== -1 || n.indexOf('uni') !== -1 ||
            n.indexOf('tom') !== -1 || n.indexOf('game') !== -1 || n.indexOf('net') !== -1) {
            interesting.push({name: m.name, base: m.base.toString(), size: m.size, path: m.path});
        }
    }
    send({type: 'mods', count: mods.length, interesting: interesting});
})();
"""

try:
    session = dev.attach("com.netease.tom")
    print("[+] attached")
except Exception as e:
    print("[!] attach failed:", e)
    # 尝试按 pid
    try:
        session = dev.attach(52554)
        print("[+] attached by pid")
    except Exception as e2:
        print("[!] attach by pid failed:", e2)
        sys.exit(1)

script = session.create_script(script_src)

def on_message(msg, data):
    if msg['type'] == 'send':
        d = msg['payload']
        if d.get('type') == 'mods':
            print(f"[mods] total={d['count']}")
            for m in d['interesting']:
                print(f"   {m['name']:35s} base={m['base']} size={m['size']:>9d} path={m['path'][-60:]}")
    else:
        print("[msg]", msg)

script.on('message', on_message)
script.load()
time.sleep(2)
try:
    session.detach()
except Exception:
    pass
print("[done]")