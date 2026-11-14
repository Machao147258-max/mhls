// Hook libcocos2dlua.so 的 XXTEA 解密核心 (STATUS.md: 0x8526a8)
// ARM so 在 0x4000... 区, frida 按绝对地址 attach
var base = ptr('0x400020e00000');
var target = base.add(0x8526a8);
console.log('[xxtea] target=' + target);

try {
    Interceptor.attach(target, {
        onEnter: function (args) {
            console.log('[XXTEA] enter');
            try { console.log('  a0=' + args[0] + ' a1=' + args[1] + ' a2=' + args[2]); } catch (e) {}
        },
        onLeave: function (ret) {
            console.log('[XXTEA] leave ret=' + ret);
        }
    });
    console.log('[xxtea] ATTACHED OK');
} catch (e) {
    console.log('[xxtea] ATTACH FAIL: ' + e);
}
