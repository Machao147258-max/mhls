// 冷启动 hook XXTEA 核心 (ARM 转译绝对地址) — 解密调用时抓参数/内存找 key
var base = ptr('0x400020e00000');
var targets = {
    'xxtea_core_8526a8': 0x8526a8,
    'xxtea_core_83a1a0': 0x83a1a0,
    'xxtea_core_8404d0': 0x8404d0,
    'xxtea_core_81c000': 0x81c000
};
var hooked = 0;
Object.keys(targets).forEach(function (name) {
    var off = targets[name];
    try {
        Interceptor.attach(base.add(off), {
            onEnter: function (args) {
                console.log('★CALL ' + name + ' args:');
                for (var i = 0; i < 8; i++) {
                    try {
                        var p = args[i];
                        var b = Array.prototype.slice.call(new Uint8Array(p.readByteArray(16)));
                        var hx = '';
                        for (var j = 0; j < b.length; j++) hx += ('0' + b[j].toString(16)).slice(-2);
                        var as = b.map(function (x) { return (x > 31 && x < 127) ? String.fromCharCode(x) : '.'; }).join('');
                        console.log('  a' + i + '=' + p + ' ' + hx + ' "' + as.slice(0, 8) + '"');
                    } catch (e) { console.log('  a' + i + '=?'); }
                }
                // 寄存器
                var c = this.context;
                console.log('  regs: rax=' + c.rax + ' rdi=' + c.rdi + ' rsi=' + c.rsi + ' rdx=' + c.rdx + ' rcx=' + c.rcx + ' r8=' + c.r8 + ' r9=' + c.r9);
            }
        });
        hooked++;
        console.log('hooked ' + name);
    } catch (e) {
        console.log('hook fail ' + name + ': ' + e);
    }
});
console.log('TOTAL HOOKED ' + hooked)