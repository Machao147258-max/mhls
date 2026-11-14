// 验证短链 + 捕获: 每 5s 打印 hits 数 (验证定时器活) + dump 明文
var memcpy = Module.findGlobalExportByName('memcpy');
var hits = [];
var pollCount = 0;
var dir = '/data/user/0/com.netease.tom/files/tomdump';
try { var t = new File(dir, 'w'); t.close(); } catch (e) { dir = '/data/local/tmp'; }

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
                        hits.push({ src: this.src, n: this.n, done: false, tries: 0 });
                    }
                }
            } catch (e) {}
        }
    }
});

function poll() {
    pollCount++;
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
                        var f = new File(dir + '/p_' + x.n + '_' + hits.indexOf(x) + '.bin', 'w');
                        f.write(full);
                        f.close();
                        x.done = true;
                        saved++;
                        console.log('★SAVED n=' + x.n + ' @' + x.src);
                    }
                }
            }
            x.tries++;
            if (x.tries > 120) x.done = true;
        } catch (e) { x.done = true; }
    });
    if (pollCount % 6 === 0 || saved > 0) console.log('POLL#' + pollCount + ' hits=' + hits.length + ' saved=' + saved);
    setTimeout(poll, 5000);
}

setTimeout(poll, 5000);
console.log('OK-TEST')