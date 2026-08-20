# scan_tom_engines.ps1 - 扫描所有 tom 进程的引擎库
$ADB = "D:\MuMuPlayer\nx_main\adb.exe"
$dev = "127.0.0.1:7555"

Write-Output "=== tom 进程 ==="
& $ADB -s $dev shell "su -c 'ps -A | grep netease.tom'"

Write-Output "=== 引擎扫描 per PID ==="
$pids = (& $ADB -s $dev shell "su -c 'pgrep -f netease.tom'").Trim().Split("`n")
foreach ($p in $pids) {
    $p = $p.Trim()
    if (!$p) { continue }
    Write-Output "== PID=$p =="
    $out = & $ADB -s $dev shell "su -c 'cat /proc/$p/maps 2>/dev/null | grep -oE \"[a-zA-Z0-9_./-]+\.so\" | sort -u | grep -iE \"cocos|lua|sec|engine|game|tom|unisec\" | head -20'"
    $out | ForEach-Object { Write-Output "   $_" }
}