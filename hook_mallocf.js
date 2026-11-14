// 强过滤 malloc hook: 只报 luac 特征 (1b 开头) + 高上限 5000
var mallocPtr = Module.findGlobalExportByName('malloc');
var n = 0;
var dir = '/data/user/0/com.netease.tom/files/tomdump';

Interceptor.attach(mallocPtr, {
    onEnter: function (args) {
        this.sz = args[0].toInt32();
    },
    onLeave: function (ret) {
        var sz = this.sz;
        if (sz > 500 && n < 5000) {
            var p = ret, idx = n++;
            setTimeout(function () {
                try {
                    var b = Array.prototype.slice.call(new Uint8Array(p.readByteArray(16)));
                    // luac 特征: 0x1b 开头 (标准/魔改 Lua 头都用 0x1b 或自定义)
                    if (b[0] === 0x1b) {
                        var hx = '';
                        for (var i = 0; i < 8 && i < b.length; i++) hx += ('0' + b[i].toString(16)).slice(-2);
                        console.log('★★LUAC? m_' + idx + '_' + sz + ' head=' + hx);
                        try {
                            var full = p.readByteArray(sz);
                            if (full) {
                                var f = new File(dir + '/L_' + idx + '_' + sz + '.bin', 'w');
                                f.write(full);
                                f.close();
                                console.log('   SAVED L_' + idx + '_' + sz + '.bin');
                            }
                        } catch (e) {}
                    }
                } catch (e) {}
            }, 8000);
        }
    }
});
console.log('OK-MALLOC-FILTER')