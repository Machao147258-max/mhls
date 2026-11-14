// 完善版: malloc hook + 8s dump + source 路径解析 + 上限 2500
var mallocPtr = Module.findGlobalExportByName('malloc');
var n = 0;
var dir = '/data/user/0/com.netease.tom/files';
var savedCount = 0;

function getSource(buf, sz) {
    // Lua 5.1 main proto: 头12B + source string (size_t=8)
    try {
        if (sz < 20) return '';
        var arr = new Uint8Array(buf);
        if (arr[0] !== 0x1b || arr[1] !== 0x4c) return '';
        var dv = new DataView(buf, 12, 8);
        var len = Number(dv.getBigUint64(0, true));
        if (len < 1 || len > 200) return '';
        var s = '';
        for (var i = 0; i < len && 20 + i < sz; i++) {
            var c = arr[20 + i];
            s += (c > 31 && c < 127) ? String.fromCharCode(c) : '?';
        }
        return s;
    } catch (e) { return ''; }
}

Interceptor.attach(mallocPtr, {
    onEnter: function (args) {
        this.sz = args[0].toInt32();
    },
    onLeave: function (ret) {
        var sz = this.sz;
        if (sz > 500 && n < 2500) {
            var p = ret, idx = n++;
            setTimeout(function () {
                try {
                    var head = p.readByteArray(8);
                    if (head) {
                        var b = Array.prototype.slice.call(new Uint8Array(head));
                        if (b[0] === 0x1b && b[1] === 0x4c) {
                            var src = getSource(p.readByteArray(Math.min(sz, 200)), Math.min(sz, 200));
                            var full = p.readByteArray(sz);
                            if (full) {
                                try {
                                    var f = new File(dir + '/L_' + idx + '_' + sz + '.bin', 'w');
                                    f.write(full);
                                    f.close();
                                    savedCount++;
                                    console.log('★SAVED L_' + idx + '_' + sz + ' src=' + src);
                                } catch (e) {
                                    console.log('★★WRITE-FAIL: ' + e);
                                }
                            }
                        }
                    }
                } catch (e) {}
            }, 8000);
        }
    }
});
console.log('OK-MALLOC-SRC')