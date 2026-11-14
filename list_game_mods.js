var mods = Process.enumerateModules();
mods.forEach(function (m) {
    try {
        if (m.path && m.path.indexOf('netease.tom') >= 0) {
            console.log('  ' + m.name + ' base=' + m.base + ' size=' + m.size);
        }
    } catch (e) {}
});
