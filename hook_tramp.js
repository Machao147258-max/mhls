// hook_tramp.js — getTrampoline 包装静态 ARM 函数 + hook 抓 key
var LF = '/data/data/com.netease.tom/files/hooklog.txt';
var f = new File(LF, 'a');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] tramp 脚本 ' + Date.now());
function hex16(p) {
    try {
        var b = p.readByteArray(16);
        var s = '';
        for (var i = 0; i < 16; i++) s += ('0' + b[i].toString(16)).slice(-2);
        return s;
    } catch (e) { return null; }
}
// 从 /proc/self/maps 找游戏 so 基址
try {
    var fr = new File('/proc/self/maps', 'r');
    var all = fr.readBytes(4096 * 64).toString();
    fr.close();
    var base = null;
    var lines = all.split('\n');
    for (var i = 0; i < lines.length; i++) {
        if (lines[i].indexOf('40002') === 0 && lines[i].indexOf('r--p') > 0 && lines[i].indexOf('com.netease.tom') > 0) {
            base = ptr(lines[i].split('-')[0]);
            break;
        }
    }
    if (!base) {
        for (var j = 0; j < lines.length; j++) {
            if (lines[j].indexOf('40002') === 0 && lines[j].indexOf('r--p') > 0) {
                base = ptr(lines[j].split('-')[0]);
                break;
            }
        }
    }
    L('[base] ' + base);
} catch (e) {
    L('[maps err] ' + e);
    var base = ptr('0x400025800000');
    L('[base fallback] ' + base);
}
try {
    var h = Process.getModuleByName('libhoudini.so');
    var itf = null;
    h.enumerateExports().forEach(function (e) {
        if (e.name === 'NativeBridgeItf') itf = e.address;
    });
    var handle = itf.add(8).readPointer();
    var getTramp = itf.add(0x18).readPointer();
    L('[handle] ' + handle + ' [getTramp] ' + getTramp);
    var nf = new NativeFunction(getTramp, 'pointer', ['pointer', 'pointer', 'pointer', 'int']);
    ['0x8ab25c', '0x8ab318', '0x8ab094', '0x8aaeac', '0x85261c'].forEach(function (off) {
        try {
            var armAddr = base.add(parseInt(off, 16));
            var out = Memory.alloc(8);
            out.writePointer(ptr(0));
            var r = nf(handle, armAddr, out, 0);
            var x = out.readPointer();
            L('[tramp ' + off + '] ret=' + r + ' x86=' + x);
            if (!x.isNull()) {
                Interceptor.attach(x, {
                    onEnter: function (args) {
                        try {
                            L('[★CALL ' + off + '] a0=' + args[0] + ' a1=' + args[1] + ' a2=' + args[2] + ' a3=' + args[3]);
                            for (var ai = 1; ai <= 3; ai++) {
                                var hx = hex16(args[ai]);
                                if (hx) L('[★MEM ' + ai + '] ' + hx);
                            }
                        } catch (e) { L('[call err] ' + e); }
                    }
                });
                L('[+ hook ' + off + ' OK]');
            }
        } catch (e) { L('[tramp ' + off + ' err] ' + e); }
    });
} catch (e) {
    L('[init err] ' + e);
}
