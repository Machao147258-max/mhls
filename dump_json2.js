// dump JSON 明文到 stdout (frida -o 落盘)
var p = ptr('0x72b5d06f92b8');
try {
    var b = p.readByteArray(41912);
    if (b) {
        var arr = Array.prototype.slice.call(new Uint8Array(b));
        // 转字符串输出 (JSON 是 ascii)
        var s = '';
        for (var i = 0; i < arr.length; i++) s += String.fromCharCode(arr[i]);
        console.log('<<<JSON-START>>>');
        console.log(s);
        console.log('<<<JSON-END>>>');
    }
} catch (e) { console.log('FAIL: ' + e); }