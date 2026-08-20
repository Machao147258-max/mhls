// tls_find.js — 枚举所有模块的 TLS/SSL 符号 (找真实 HTTPS 实现)
var LF = '/data/data/com.netease.tom/files/tls_find.txt';
var f = new File(LF, 'a');
function L(s) { try { f.write(s + '\n'); f.flush(); } catch (e) {} }
L('[+] tls_find start');

Process.enumerateModules().forEach(function (m) {
    var name = m.name.toLowerCase();
    if (!/ssl|crypto|tls|net|http|curl|nls|mmtls|gnutls|mbedtls|nss|wolf/.test(name)) return;
    var hits = [];
    try {
        m.enumerateExports().forEach(function (e) {
            if (/^(SSL_|ssl3_|tls1_|tls_|BIO_|CRYPTO_|EVP_|ngssl|nd_send|NLS|nls_|mmtls)/.test(e.name)) {
                hits.push(e.name);
            }
        });
    } catch (e) {}
    if (hits.length) {
        L('[MOD] ' + m.name + ' base=' + m.base);
        hits.slice(0, 40).forEach(function (h) { L('  ' + h); });
    }
});
L('[+] done');