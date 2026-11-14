// 静默轮询版 v2: hook 零打印 → 每 60s 轮询 src 是否明文 → dump app 目录
var memcpy = Module.findGlobalExportByName('memcpy');
var hits = [];
var dir = '/data/user/0/com.netease.tom/files/tomdump';
try { var t = new File(dir, 'w'); t.close(); } catch (e) { dir = '/data/local/tmp'; }

Interceptor.attach(memcpy, {
    onEnter: function (args) {
        this.dst = args[0];
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
    }
});

function poll() {
    var saved = 0;
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
                        var f = new File(dir + '/p_' + hits.indexOf(x) + '_' + x.n + '.bin', 'w');
                        f.write(full);
                        f.close();
                        x.done = true;
                        saved++;
                        console.log('★SAVED n=' + x.n + ' @' + x.src);
                    }
                }
            }
        } catch (e) {}
    });
    if (saved > 0) console.log('poll saved=' + saved + ' totalHits=' + hits.length);
}

setInterval(poll, 60000);
console.log('OK-POLL dir=' + dir);