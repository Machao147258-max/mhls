// tb_dump: 把含 Lua5.1 字节码的内存段整段 dump 到游戏 cache 目录
function log(m) { console.log(m); }

setTimeout(function () {
    log('[*] tb_dump attach ok');
    var outdir = '/data/data/com.netease.tom/cache/';
    var pat = '1b 4c 75 61 51';

    // 先建目录(游戏进程自有权限)
    try { new File(outdir + '.probe', 'w').write('ok'); } catch (e) { log('[-] cache 不可写: ' + e); }

    var seen = {};
    var idx = 0;
    Process.enumerateRanges('rw-').forEach(function (r) {
        if (r.size > 256 * 1024 * 1024) return;
        var hits = null;
        try { hits = Memory.scanSync(r.base, r.size, pat); } catch (e) { return; }
        if (!hits || !hits.length) return;
        if (seen[r.base.toString()]) return;
        seen[r.base.toString()] = true;
        var name = outdir + 'dump_' + idx + '_' + Math.round(r.size / 1024) + 'k.bin';
        idx++;
        try {
            var b = r.base.readByteArray(r.size);
            var f = new File(name, 'wb');
            f.write(b); f.close();
            log('[+] dumped ' + name + '  ' + r.size + ' bytes  (' + hits.length + ' 个chunk头)');
        } catch (e) {
            log('[-] write fail ' + name + ' : ' + e);
        }
    });
    log('[*] done, 共 ' + idx + ' 段');
}, 2500);