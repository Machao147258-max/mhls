var mods = Process.enumerateModules();
console.log('[tom] modules=' + mods.length);
mods.forEach(function (m) {
    if (/cocos|lua|unisec|netease|runtime|tom|dun/i.test(m.name)) {
        console.log('  ' + m.name + ' base=' + m.base + ' size=' + m.size);
    }
});
