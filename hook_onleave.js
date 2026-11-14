// 纯 onLeave 节流版: 每次 memcpy onLeave 后节流检查 hits (无顶层定时器)
var memcpy = Module.findGlobalExportByName('memcpy');
var hits = [];
var lastCheck = 0;
var savedCount = 0;
var dir = '/data/user/0/com.netease.tom/files/tomdump';
try { var t = new File(dir, 'w'); t.close(); } catch (e) { dir = '/data/local/tmp'; }

function checkAndDump() {
    var now = Date.now();
    if (now - lastCheck < 3000) return;  // 3s 节流
    lastCheck = now;
    hits.forEach(function (x) {
        if (x.done) return;
        try {
            var b = x.src.readByteArray(8);
            if (b) {
                var a = Array.prototype.slice.call(new Uint8Array(b));
                var isCipher = (a[0] === 0x58 && a[1] === 0x31 && a[2] === 0x56 && a[3] === 0x35);
                if (!isCipher && a[0] !== 0x00 && a[0] !== 0xff) {
                    var full = x.src.readByteArray(x.n);
                    if (full) {
                        var f = new File(dir + '/p_' + x.n + '_' + hits.indexOf(x) + '.bin', 'w');
                        f.write(full);
                        f.close();
                        x.done = true;
                        savedCount++;
                        console.log('★SAVED n=' + x.n + ' @' + x.src + ' total=' + savedCount);
                    }
                }
            }
        } catch (e) { x.done = true; }
    });
}

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.src = args[1];
        this.n = args[2].toInt32();
    },
    onLeave: function (ret) {
        if (this.n > 1000) {
            try {
                var h = this.src.readByteArray(8);
                if (h) {
                    var arr = Array.prototype.slice.call(new Uint8Array(h));
                    if (arr[0] === 0x58 && arr[1] === 0x31 && arr[2] === 0x56 && arr[3] === 0x35) {
                        hits.push({ src: this.src, n: this.n, done: false });
                    }
                }
            } catch (e) {}
        }
        checkAndDump();  // 每次 onLeave 节流检查
    }
});
console.log('OK-ONLEAVE')