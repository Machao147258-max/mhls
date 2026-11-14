// Hook XXTEA 解密核心 + 抓参数 (密钥/密文/明文)
var base = ptr('0x400020e00000');
var target = base.add(0x8526a8);
console.log('[xxtea] target=' + target);

// 抓解密核心的所有参数 + 尝试 dump 明文缓冲
Interceptor.attach(target, {
    onEnter: function (args) {
        this.t = Date.now();
        console.log('===== [XXTEA] enter t=' + this.t);
        try {
            for (var i = 0; i < 6; i++) {
                console.log('  a' + i + '=' + args[i]);
            }
        } catch (e) { console.log('  arg read fail: ' + e); }
    },
    onLeave: function (ret) {
        console.log('  [XXTEA] leave ret=' + ret + ' dt=' + (Date.now() - this.t) + 'ms');
    }
});

// 同时 hook 常见 Lua 加载点: luaD_call / luaV_execute 入口 (教学场景活跃)
console.log('[xxtea] ready');
