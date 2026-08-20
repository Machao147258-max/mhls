// hook_full_net.js — 全量网络包捕获 (send/recv/SSL_read/SSL_write + hex + 文本)
var LF = '/data/data/com.netease.tom/files/hook_full.txt';
var f = new File(LF, 'a');
function L(s) {
    try { f.write(s + '\n'); f.flush(); } catch (e) {}
}
L('[+] full_net ' + Date.now());

function hex(b, max) {
    max = max || 64;
    var s = "";
    for (var i = 0; i < b.length && i < max; i++) s += ("0" + b[i].toString(16)).slice(-2);
    return s + (b.length > max ? '...(+' + (b.length - max) + ')' : '');
}
function toStr(b) {
    var s = "";
    for (var i = 0; i < b.length; i++) {
        var c = b[i];
        if (c >= 32 && c < 127) s += String.fromCharCode(c);
        else if (c === 0) s += ' ';
        else s += '.';
    }
    return s;
}

function dump(tag, buf, len) {
    if (!buf || len <= 0) return;
    try {
        var b = buf.readByteArray(Math.min(len, 512));
        var bytes = new Uint8Array(b);
        L('[' + tag + '] len=' + len + ' hex=' + hex(bytes, 96) + ' str=' + toStr(bytes.slice(0, 64)));
    } catch (e) {}
}

['send', 'sendto', 'write'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onEnter: function (a) {
                dump('SEND', a[1], a[2].toInt32());
            }
        });
        L('[+] ' + n + ' hooked (send)');
    } catch (e) {}
});
['recv', 'recvfrom', 'read'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onLeave: function (ret) {
                if (ret.toInt32() > 0) {
                    dump('RECV', this.buf, ret.toInt32());
                }
            },
            onEnter: function (a) {
                this.buf = a[1];
            }
        });
        L('[+] ' + n + ' hooked (recv)');
    } catch (e) {}
});
// SSL (HTTPS)
['SSL_read', 'SSL_write'].forEach(function (n) {
    try {
        var p = Module.getGlobalExportByName(n);
        Interceptor.attach(p, {
            onEnter: function (a) {
                if (n === 'SSL_write') dump('SSL_W', a[2], a[3].toInt32());
            },
            onLeave: function (ret) {
                if (n === 'SSL_read' && ret.toInt32() > 0) {
                    dump('SSL_R', this.buf, ret.toInt32());
                }
            }
        });
        L('[+] ' + n + ' hooked');
    } catch (e) {}
});
try {
    var p = Module.getGlobalExportByName('connect');
    Interceptor.attach(p, {
        onEnter: function (a) {
            var sockaddr = a[1];
            try {
                var fam = sockaddr.readU16();
                if (fam === 2) {
                    var port = (sockaddr.add(2).readU16() & 0xff) * 256 + (sockaddr.add(2).readU16() >> 8);
                    var ip = sockaddr.add(4).readByteArray(4);
                    var u = new Uint8Array(ip);
                    L('[CONN] ' + u.join('.') + ':' + port);
                }
            } catch (e) {}
        }
    });
    L('[+] connect hooked');
} catch (e) {}
L('[+] FULL_NET 就绪');