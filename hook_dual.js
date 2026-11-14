// Hook luaU_undump (脚本加载必经) + XXTEA 核心双钩
var base = ptr('0x400020e00000');
var undump = base.add(0x676b80);   // STATUS: luaU_undump @0x676b80
var xxtea = base.add(0x8526a8);    // STATUS: XXTEA 核心

console.log('[dual] undump=' + undump + ' xxtea=' + xxtea);

try {
    Interceptor.attach(undump, {
        onEnter: function (args) {
            console.log('===== [UNDUMP] enter');
            try { console.log('  a0=' + args[0] + ' a1=' + args[1] + ' a2=' + args[2] + ' a3=' + args[3]); } catch (e) {}
        },
        onLeave: function (ret) {
            console.log('  [UNDUMP] leave ret=' + ret);
        }
    });
    console.log('[dual] undump ATTACHED');
} catch (e) { console.log('[dual] undump FAIL: ' + e); }

try {
    Interceptor.attach(xxtea, {
        onEnter: function (args) {
            console.log('===== [XXTEA] enter');
            try { console.log('  a0=' + args[0] + ' a1=' + args[1] + ' a2=' + args[2] + ' a3=' + args[3]); } catch (e) {}
        },
        onLeave: function (ret) {
            console.log('  [XXTEA] leave ret=' + ret);
        }
    });
    console.log('[dual] xxtea ATTACHED');
} catch (e) { console.log('[dual] xxtea FAIL: ' + e); }
