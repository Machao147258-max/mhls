// 秒级 dump 版: hook memcpy 捕获 X1V5fzTo → 5s 后 dump src (解密原地)
// 只 dump 头非 X1V5fzTo 的 (已解密明文), 减少输出
var memcpy = Module.findGlobalExportByName('memcpy');
var n = 0;

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 1500) {  // 只要大脚本
            try {
                var head = this.src.readByteArray(8);
                if (head) {
                    var h = Array.prototype.slice.call(new Uint8Array(head));
                    if (h[0] === 0x58 && h[1] === 0x31 && h[2] === 0x56 && h[3] === 0x35) {
                        var src = this.src, sz = this.n;
                        n++;
                        setTimeout(function () {
                            try {
                                var b2 = Array.prototype.slice.call(new Uint8Array(src.readByteArray(16)));
                                var hx = '';
                                for (var i = 0; i < b2.length; i++) hx += ('0' + b2[i].toString(16)).slice(-2);
                                var isCipher = (b2[0] === 0x58 && b2[1] === 0x31 && b2[2] === 0x56 && b2[3] === 0x35);
                                if (!isCipher && b2[0] !== 0x00) {
                                    // 明文! 完整 dump
                                    var full = src.readByteArray(sz);
                                    if (full) {
                                        var arr = Array.prototype.slice.call(new Uint8Array(full));
                                        var s = '';
                                        for (var j = 0; j < arr.length; j++) s += String.fromCharCode(arr[j]);
                                        console.log('<<<PLAIN n=' + sz + ' ' + hx.slice(0, 16) + '>>>');
                                        console.log(s.slice(0, 2000));
                                        console.log('<<<END>>>');
                                    }
                                }
                            } catch (e) {}
                        }, 5000);
                    }
                }
            } catch (e) {}
        }
    }
});
console.log('OK-FAST');