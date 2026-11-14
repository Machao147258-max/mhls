var mods = Process.enumerateModules();
var c = 0;
mods.forEach(function (m) {
    try {
        if (m.path && (m.path.indexOf('/data/') === 0 || m.path.indexOf('/data/app') >= 0)) {
            c++;
            if (c <= 40) console.log('  ' + m.name + ' @ ' + m.base + ' path=' + m.path);
        }
    } catch (e) {}
});
console.log('[tom] total /data mods=' + c);
