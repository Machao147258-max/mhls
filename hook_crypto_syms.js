// symbol 枚举 + 自动 hook Crypto/Xxtea 类方法 — 解密时读参数找 key
var lib = Process.findModuleByName('libcocos2dlua.so');
console.log('lib: ' + (lib ? lib.base : 'NOT FOUND'));
var hooks = 0;

function tryHook(name, addr) {
    try {
        Interceptor.attach(addr, {
            onEnter: function (args) {
                // 打印前 6 个参数 (指针解引用 16B)
                var out = 'HIT ' + name;
                for (var i = 0; i < Math.min(6, args.length); i++) {
                    try {
                        var b = Array.prototype.slice.call(new Uint8Array(args[i].readByteArray(16)));
                        var hx = '';
                        for (var j = 0; j < b.length; j++) hx += ('0' + b[j].toString(16)).slice(-2);
                        var as = b.map(function (x) { return (x > 31 && x < 127) ? String.fromCharCode(x) : '.'; }).join('');
                        out += ' | a' + i + '=' + hx.slice(0, 16) + ' "' + as.slice(0, 8) + '"';
                    } catch (e) { out += ' | a' + i + '=?'; }
                }
                console.log(out);
            }
        });
        hooks++;
        return true;
    } catch (e) { return false; }
}

if (lib) {
    var syms = lib.enumerateSymbols();
    var hits = [];
    syms.forEach(function (s) {
        var n = s.name.toLowerCase();
        if (n.indexOf('xxtea') >= 0 || n.indexOf('crypto') >= 0 || n.indexOf('decrypt') >= 0 || n.indexOf('encrypt') >= 0) {
            hits.push(s);
        }
    });
    console.log('crypto symbols: ' + hits.length);
    hits.forEach(function (s) {
        console.log('  SYM ' + s.address + ' ' + s.name);
        if (hooks < 12) tryHook(s.name, s.address);
    });
}
console.log('HOOKED ' + hooks)