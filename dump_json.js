// dump JSON 明文 (0x72b5d06f92b8, 41912 字节) 完整内容到设备文件
var p = ptr('0x72b5d06f92b8');
try {
    var b = p.readByteArray(41912);
    if (b) {
        var f = '/data/local/tmp/tom_json_plain.bin';
        var w = new File(f, 'w');
        w.write(b);
        w.close();
        // 打印开头 200 字节确认
        var arr = Array.prototype.slice.call(new Uint8Array(b));
        var head = '';
        for (var i = 0; i < 100 && i < arr.length; i++) head += String.fromCharCode(arr[i]);
        console.log('SAVED ' + f + ' size=' + arr.length);
        console.log('HEAD: ' + head.slice(0, 100));
    }
} catch (e) { console.log('FAIL: ' + e); }