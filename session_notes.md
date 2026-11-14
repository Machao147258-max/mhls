# 本会话新增确认 (2026-08-11 下午, 实证于 launcher_raw.luac = s631@0x748)# 引擎: RUNTIME so 主循环 0x6091d4(取指)/0x60933c(取指循环), 跳转表 0xcd2c84 (idx=op-3, 2B有符号×4, 基准 0x6092a0)
# 格式表 0xcd3820: 低2位=mode(0 ABC/1 ABx/2 AsBx), bit2-3=f2, bit4-5=f4 (操作数校验子标志), bit6-7=前置分路
#  IMPORTANT: 本 VM 的 B/C 字段与标准 Lua 相反 — "C 中心":
#   op7  MOVE  R[A] = R[C]   (B 恒 0; f2=0 校验 B==0)
#   op17 GETTABLE R[A] = R[C][B]  (B=键 256+k 或寄存器, C=表; f2=3)
#   op33 SELF  与 GETTABLE 同族 (0x6c)
#   op4  CALL  fn=R[A], nargs=B+1 (args R[A+1..A+B+1]), nresults=C-1 (C=0 → multret)
#     实证: [319] CALL A=35 B=2 C=4 → format(k92, R24, R32) 3 参数 ✓
#     [39] fn=R7(string.len) B=0 → 1 参数 R8 ✓
#   op20 LOADK R[A] = k[Bx] (Bx 直接索引, 无 -256!)
#   op34 GETGLOBAL R[A] = global[k[Bx]] (直接索引)
#   op12 SETGLOBAL global[k[Bx]] = R[A]   ★ 新确认 (ABx, 直接索引)
#   op0  LT    R[B] < R[C] (B/C 均可 256+k 常量; A=跳转极性: A=0 → 条件真时跳)
#     实证: [283] LT A=0 B=33 C=339(k83=0.0) → R33 < 0.0
#   op16 二元拼接 R[A] = R[C] .. R[B]   ★ 新确认 (B/C 均寄存器, 常量须先 LOADK)
#     实证: [306] R32=R32..'_uiauto'; [313] R32=R32..'_module'; [323] R31='windows'..R32 (PREFIX)
#   op22 EQ   R[B] == R[C] (B/C 常量感知), A=1 → 不等跳
#   op14 TEST R[A] 真值; B=0 常规
#   op10 LOADIMM 疑似 R[A] = k[Bx] 或立即数 (未定)
# 其他:
#   RUNTIME so 加密核心 0x852804 = 诱饵 (target=(52//n)*DELTA+0xB54CDA56 非 DELTA 倍数 → 死循环, 反调试)
#   解密核心 0x8526a8 = 标准 XXTEA 解密 (sum 从 rounds*DELTA 递减, y=v[p] 更新, k[(p^e)&3], p0: z=v[n-1], y=v[1], k[e&3])
#   文件格式: X1V5fzTo + 4B 随机(每文件独立, 非 0) + XXTEA 密文 (密文从 offset 12 起, n=ceil(len/4))
#   黄金对: common_utils 结构=3574B (parse_end=3574, 文件 1.6MB 其余为尾部数据) ↔ 217a71cb...bin (3588B) ✓ 有效
#   role.lua 结构=53813B; UGCSystem dump 损坏(常量区被堆覆盖); launcher 主函数 928 指令无算术 op
#   APK 内 assets/filelist_*.json 无路径映射; 脚本路径映射在加密代码内部
#
# ★ 本会话重大发现 (2026-08-11 傍晚):
#   1. 全局槽号方案: common_utils 主函数 sizek=0/sizep=0/空debug(结构 3574B 自洽),
#      但代码引用常量 → GETGLOBAL Bx = 全局槽号, 非常量索引!
#      全局名字表 = launcher 常量表顺序(require=0, cjson=1, math=2, ...)
#      用该表反编译 common_utils 子函数 → 完全可读(isSupportAstc 逻辑还原!)
#      → 所有脚本共享全局名字表; 各脚本反编译需此表
#   2. Z3 数学路线确认死路: 25字×8轮小文件单字约束 38s 超时, 全链/零字窗口全 unknown
#      (z3 对随机函数反演不可行; 894 字全链更无望)
#   3. 待查: 0x8aa378 / 0x8aa4a4 (0x8ab25c 流式路径调用) 可能是真实加密核心(非诱饵)
#   4. 待查: version.bin 明文格式需从 launcher 反编译代码反推(version.json 解析逻辑)
#   5. launcher_rev.py = 黄金验证反编译器(已确认语义), 输出 launcher_rev_out.txt (18.7KB, 可读)
#      REV_OUT2/ = 批量反编译输出 (role 202KB / GmSystem / SquareSystem / common_utils)

# ★★ 2026-08-15 深夜: XXTEA 密文捕获突破 (frida hook memcpy)
#   hook libc memcpy → 捕获 X1V5fzTo 密文拷贝流 (14+ 脚本, 644B~39808B):
#     HIT n=39808 src=0x72b5cfc9fdf8 dst=0x72b337f78640 等
#   DST 在 memcpy onLeave 时仍是 X1V5fzTo (密文搬移, 解密延迟/独立调用)
#   LATE-DST (5s后): 部分缓冲已解密 → "TSYS" 明文结构 (54535953 1b 00 00 ... android)
#     部分仍 X1V5fzTo (缓冲复用/未解密原地)
#   ★ 解密非原地: 密文拷贝到 dst 后, 解密输出在别处 (需找解密函数输出缓冲)
#   frida 读内存通道: attach 后 readByteArray 可读 (dd /proc/mem 对新进程 I/O error!)
#   ★ /proc/mem 不可读 = 易盾新版冷启动保护 (force-stop 后进程 mem 全 I/O error)
#   frida 注意事项: attach 前必重启 nsv11; 单次 attach 内 setTimeout(5s) 可用 (长轮询会超时)
#   hook ARM so 代码: 绝对地址 base+offset 可 attach (0x8526a8 XXTEA 核心 ATTACHED 但 0 调用 — 诱饵或 houdini 翻译区)

# ★★★ 2026-08-16 凌晨: 明文 luac 完整捕获管线打通!!! (malloc hook 方案)
#   ★ 方法: hook libc malloc (NOT memcpy!) → 捕获 >500B 分配 → onLeave 内 setTimeout(8000)
#     读分配缓冲 → 头 0x1b 0x4c (Lua 5.1: 1b4c756151000104 04040800) → 完整 dump 到
#     /data/user/0/com.netease.tom/files/L_xxx.bin (app 私有目录可写!)
#   ★ malloc hook 低频稳定不崩 (memcpy hook 高频必崩 agent); 顶层 setInterval 失效,
#     onLeave 内 setTimeout(8s) 可靠 (与 capture2 的 5s 验证一致)
#   ★ 游戏冷启动 (缓存缺失清空 resource/) 时 700+ 脚本全量解密 → malloc 大量 luac 缓冲
#     缓存存在时只加载启动必需小脚本 (4096/3512/896B 模式)
#   ★ 结构: 标准 Lua 5.1 头 + 紧凑 size (source 长度=4B 小端, rd_tstr <I) — launcher_rev.py 完全兼容
#   ★ 成果: 73/73 luac 反编译成功 (launcher_rev.py 批量) → 可读 Lua!
#     - 路径映射表: @src/catchGame/{data,systems,network,sdk,utils,uiExtend,box2d}/...
#       例: ClanRank.lua = class('ClanRank', RankBase) + 15 方法 (onCreate/reqRank/reqClanRankList)
#     - 含 role.lua / string_config.lua / protoc.lua / ModuleSystem / NewCreditSystem / queue.lua 等
#   ★ 剧本: 重启游戏 → 加载完成或加载早期 attach (新进程首次 attach 必成功; attach 过=坏死需重启)
#     清缓存=全量重解密(大脚本 3.5MB! 但 OOM 风险); 游戏 OOM 被杀时已保存文件完好
#   ★ 待办: 拉高 MuMu 内存防 OOM 抓 3.5MB 大脚本 (UI 框架); nx_device/15.0/configs 无内存字段
#     内存配置在 MuMu 前端 UI (设置→性能)
# ★ 2026-08-16 密钥路线终结结论 (避免重复踩坑)
# 1. ★候选 key 全是文件名误读: key_test_cands.py 的 5 个 16B hex = apk_launcher 里
#    X1V5 密文文件的文件名 (f3e08b5119358a8f58f17a678759f60c.bin 47028B 等)!
#    早期把"文件 hash 名"当 key 候选 → 全部无效 (12 密文 x 5 key x 2 模式 = 0 命中)
# 2. ★ARM so hook 死路确认: 0x8526a8 冷启动 attach 0 CALL — ARM 代码经 houdini
#    翻译执行, 原地址不经过; 其他地址 unable to intercept (翻译区非指令边界)
# 3. 密文格式: X1V5fzTo(8B) + 4B 随机 + 载荷; 载荷长度 == 明文 (无 +8 标准XXTEA特征)
#    非标准 XXTEA/自定义; 4B 随机同脚本恒定 (非真随机, 文件专属)
# 4. size 配对不可靠: 同 size 明文/密文大量存在但不同脚本 (184 候选对全假)
# 5. 差分攻击前提缺失: 无确定同脚本明文/密文对 (launcher_raw 18525B 密文不在捕获集)
# 6. 最终状态: 73 脚本明文反编译 (完整可读) + 219 明文/4248 密文 (带 size 未配对)
#    key 未破 → 离线全量解密未达成; 后续更新需重新 hook 抓取 (剧本已验证可用)
