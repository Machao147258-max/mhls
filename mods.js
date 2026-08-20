// mods.js — 枚举进程全部 so: 非系统库 + 文件路径 (找自研 TLS)
var LF = '/data/data/com.netease.tom/files/mods.txt';
var f = new File(LF, 'a');
function L(s) { try { f.write(s + '\n'); f.flush(); } catch (e) {} }
L('[+] mods ' + Date.now());
Process.enumerateModules().forEach(function (m) {
    // 非系统库 (不在 /system /apex)
    if (/\/system\//.test(m.path) || /\/apex\//.test(m.path)) return;
    L(m.base + '  ' + m.name + '  ' + m.path);
});
L('[+] done');