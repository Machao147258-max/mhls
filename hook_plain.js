// 抓 X1V5fzTo 拷贝后 dst 解密结果 (轮询 500ms, 捕获明文 luac 头)
var memcpy = Module.findGlobalExportByName('memcpy');
var c = 0;

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 500 && c++ < 50) {
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    var magic = String.fromCharCode.apply(null, h);
                    if (magic === 'X1V5fzTo') {
                        var src = this.src, dst = this.dst, n = this.n;
                        console.log('★★★★★ X1V5fzTo n=' + n + ' src=' + src + ' dst=' + dst);
                        // 轮询 dst: 解密后应变为 luac (1b 0x4c 0x75 0x61 或 0x1bLua)
                        var tries = 0;
                        var iv = setInterval(function () {
                            tries++;
                            try {
                                var b = dst.readByteArray(8);
                                if (b) {
                                    var d = Array.prototype.slice.call(new Uint8Array(b));
                                    var hex = d.map(function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
                                    var ascii = String.fromCharCode.apply(null, d);
                                    // luac 头特征: 1b 4c 75 61 (0x1bLua) 或 魔改
                                    if (d[0] === 0x1b || (d[0] !== 0x58 && ascii.indexOf('X1V5') !== 0)) {
                                        console.log('  ★Dst t+' + (tries * 100) + 'ms: ' + hex + ' "' + ascii + '"');
                                        clearInterval(iv);
                                        // dump 前 256B 明文
                                        try {
                                            var full = dst.readByteArray(Math.min(256, n));
                                            if (full) {
                                                var fb = Array.prototype.slice.call(new Uint8Array(full));
                                                var fh = fb.map(function (x) { return ('0' + x.toString(16)).slice(-2); }).join('');
                                                console.log('  PLAIN256: ' + fh);
                                            }
                                        } catch (e) {}
                                    }
                                }
                            } catch (e) { clearInterval(iv); }
                            if (tries > 20) clearInterval(iv);
                        }, 100);
                    }
                }
            } catch (e) {}
        }
    }
});
console.log('[v3] ready');
