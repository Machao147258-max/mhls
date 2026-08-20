# 猫和老鼠逆向工程 — 阶段总结(2026-08-08)

## 一、已攻破(全部有证据)

### 1. 游戏技术栈
- 引擎: Cocos2d-x Lua(Java 入口 `org.cocos2dx.lua.AppActivity`, `libcocos2dlua.so` ARM64, 模拟器上过 Houdini 转译)
- Lua 版本: 5.1 头(int=4, size_t=4, instr=4, num=8), **但指令集是魔改的(自定义 VM)**
- 包名 com.netease.tom, 当前版本 7.49.2(设备)/ 7.45.0(APK), 项目代号 h18
- 补丁机制: app_ntp0/7.49.2_300/(Java dex + libunisec_x86_64.so), 设备自更新

### 2. 脚本加密(X1V5fzTo)
- 所有资源(脚本 + hotfix json + 配置)统一 8 字节魔数 `X1V5fzTo` + 强加密载荷(熵 7.997, 非 XOR/RC4 弱加密)
- 密钥不在任何静态可见位置(arm64 库无魔数字符串, 运行时构造)
- **但解密后的 luac 缓冲必然在内存** → 内存抓取路线成立

### 3. 抓取管线(已全通, 零注入)
- 纯 `/proc/PID/mem` dd 读取(一次 su 脚本跑完所有段), 无 agent 无 frida
- 段选择: 匿名 + scudo 池 1-32MB(maps 正则过滤)
- 抓到过: 多轮 10 个 chunk(含 199KB 大文件)、6 个干净 chunk
- 工具: `min_capture.py`(抓取+segmap)、`extract_chunks.py`(按结构提取)、`round_capture.py`(多轮)

### 4. 反作弊(unisec)画像
- libunisec(易盾系, arm64 原版 + ntp x86_64 变体): 模块名特征扫描、读 /proc/net/tcp、watchdog 线程(trace_stack/StackManager/dTi)
- 封号机制: 行为上报式(上报 unisec-inner.nie.netease.com) + **设备指纹连坐**
- 关键: unisdk_device_id = d3e4d3be538c705c **对所有常规修改免疫**(android_id/serial/nemud.device.id/pm clear 全无效), 只能靠新 MuMu 实例换 VM 身份
- 触发红线: 进程内 agent + 全内存扫描(两次封号实锤); 纯 dd /proc 读未触发

### 5. 自定义 Lua VM 格式(反汇编自引擎 luaU_undump)
- 函数体字段顺序 = 标准 5.1: source → linedefined → lastlinedefined → nups/numparams/is_vararg/maxstack(4×char) → sizecode → code → sizek → 常量(tt≤4) → debug
- 常量 16B/TValue(64位), 跳转表 @0xd55f20
- **指令集自定义**(opcode 100 之类, 数据直接嵌指令), 标准解码无效

## 二、断点(待攻)

### 自定义指令集语义
- luaV_execute 的分发在 stripped 引擎里, 需深度静态 RE(capstone 已就绪, find_undump.py 定位到 luaU_undump @0x676b80)
- 思路: 找到 VM 主循环的分发跳转表(rodata 指针簇, 0xd7c060 是误报, 需再找)或按 handler 特征逐个映射

## 三、工具清单(工作区)
- min_capture.py — 低噪抓取(单 su)
- round_capture.py — 多轮抓取
- extract_chunks.py — luac 结构提取
- proto_extract.py — Proto 指针解析(待 segmap 一致时用)
- dex_strings.py — dex 字符串表
- find_undump.py / lua51_disasm.py — 引擎反汇编辅助
- unluac(已编译到 C:\Users\20751\tools\unluac-out) — 反编译(等指令映射)

## 三、API/网络情报(2026-08-08 二轮)
- 游戏业务服: 45.253.181.216:28363 (TCP, crashhunter.di); Echo 网关: 42.186.48.31:35001 等 UDP
- unisdk 协议模板: protocol.unisdk.netease.com/tpsl/android_class (SDK类全集 5.5KB, ios_class 也在), /api/template/v{1..100}/latest.json 全可达
- httpdns: mbdl.update.netease.com/httpdns.mbdl (大陆 103.71.201.4); hdserver2: 1.95.233.187 等
- grs feature: g0.gsf.easebar.com/feature/query.json (pharos 规则, 确认 h18=猫和老鼠)
- 易盾链: whoami → ye.dun.163yun.com/v1/oneclick/preCheck (一键登录), /v1/preCheck; 服务端判定不可客户端伪造
- matrix clientlog 200 通; nglbs 需 gameid+经纬度(格式未明); unisec 上报 403(需内网)
- 结论: 核心业务 API = 自定义 TCP 二进制协议, 需 tcpdump 抓包解析

## 四、关键数据位置
- 设备 APK: C:\Users\20751\Desktop\猫和老鼠\device_base.apk (1.9GB, 7.45.0)
- 抓取数据: C:\Users\20751\tomdump\dd_live_1973\ (676 段 + segmap.json, 128KB-32MB 全匿名段)
- 扫掠数据: C:\Users\20751\tomdump\sweep_1973\ (r1-r3 各 6 chunk, 4 轮后 job 被终止)
- **唯一脚本全集: C:\Users\20751\tomdump\ALL_SCRIPTS\ (14 个)**
- 加密脚本全集: APK assets/package/src/*.bin (10699 个, X1V5fzTo)
- 清单: files/filelist_high.json (41036 项, 无 URL)
- CDN: h18.gph.netease.com(仅旧版 hotfix 可拉, 新版脚本包 URL 未找到)
- 设备指纹: android_id/serial 已换, nemud.device.id 需新实例

## 四.5、CDN 全量拉取成功(2026-08-08)
- **CDN 模式破解**: https://h18.gph.netease.com/patch.{patch_version}.publish/resource/{file}
- 全量下载: 10,950/10,950 脚本 (41.3MB, md5 全校验通过, 0 失败) → C:\Users\20751\tomdump\cdn_pull\
- 运行时 filelist (33.6MB, 当前版本) → device_runtime\filelist_high.json
- 运行时配置(edge_server_list/hotfix_list/module.json/ntunisdk_so_uuids) → device_runtime\
- **引擎符号表**: 58,253 个符号(含混淆名+地址) → engine_symbols.json
- **引擎解密器状态**: 魔数 X1V5fzTo 在任何文件里无完整/拆分形式(运行时构造);
  引擎确认含 ARM 硬件 AES(AESE/AESD 指令);
  luaU_undump @ 0x676b80(函数体解析器 @0x67657c, 结构=标准5.1, 指令集自定义);
  section headers 混淆但 PT_DYNAMIC 完好(dynsym 可用);
  发现 network_socket::Crypter/RSACrypter、CCryptRc4、userext::Crypto* 类 RTTI

## 四.6、加密分析结论(2026-08-08 三攻)
- **已排除**: 固定密钥流密码(XOR/RC4) — 300 文件前 12 字节密钥流全不同
- **已排除**: 文件内嵌 key + XOR/RC4(魔数后 8/16/24/32B 作 key 全试)
- **已排除**: 引擎主代码硬件 AES(0x400000-0x1000000 密集代码区 0 条 AESE/AESD/AESMC/AESIMC; 之前 42 条全是数据误报)
- **已排除**: 软件 AES S-box 静态表
- **已确立**: 每文件独立随机 IV/密钥; 载荷熵 7.997 均匀; 疑似 AES-CBC/CTR(全局 key + 每文件 IV) 或自定义算法
- **引擎结构**: section headers 混淆, PT_DYNAMIC 完好, dynsym 58,253 符号(混淆名+地址已存档 engine_symbols.json)
- **关键锚点**: luaU_undump=0x676b80, LoadInt=0x676504, LoadBlock=0x676428, LoadString=0x676468, LoadFunction=0x67657c; CCryptRc4 vtable=0x1035920(方法@0x618e38 等, RELRO 重定位解出); RSACrypter vtable=0x1036910; 构造函数 thunk 用 0xd4d000 跳转表分发
- **剩余路径**: ① 深度静态 RE 挖全局 key(小时级) ② 运行时 hook ntp Java 层解密(若解密在 Java) ③ ARM 引擎运行时 hook(houdini 阻断)

## 四.7、加密攻坚第二波(2026-08-08 深夜)
- **确认引擎用 XXTEA 家族**(0x8aaeac 解密核心: 标准 0x9E3779B9 delta, 52/count+6 轮, v[p]-mx 循环; 0x8ab094 加密核心)
- **完全破译 XXTEAUtil 密钥构造**: 基串 0xd055d0 + 偏移表 {0x01,0x25,0x29,0x28,0x02,0x25,0x02,0x20,0x21,0x23,0x24,0x22,0x27,0x29,0x27,0x01} → 取每字符 → **KEY = 6bb4c7d132b432820cc35d8e6cc76c6b**(array2 校验串 = 6d0c21b4553d3abe)
- **但 KEY1 解不开资源文件**(穷举: key 前缀 6-16/补0/补ff/倒序/零key/文件内嵌key/字符串key, 偏移 0-35, 长度字校验全失败) → XXTEAUtil 是**网络层**密钥
- **穷举排除**: 硬件 AES(0条指令)、软件 AES(无S-box)、固定密钥流、rodata 全部 16B 窗口作 XXTEA key(2.5M 窗口×2 目标)、已知明文 AES key 扫描(320万窗口)、魔数单字节 XOR 编码(256 全无)、RC4
- **新发现**: res_high_new 资源(8,055 个)用 **FETJ** 头([4B FETJ][u32 1][数据]),与 src 的 X1V5fzTo 不同格式; 内存缓存用 X1V5fzTo 作内部标记
- **内存取证突破**: 17 个内存段含魔数 + 文件路径字符串(s516 = birthday_guide_p0.astc 完整路径!); CDN 下载 md5 验证通过
- **结论**: 资产密文 = 运行时构造密钥的自定义/混淆算法; 静态挖 key 需数小时(找魔数构造代码 → 解密器 → key)

## 四.8、内存 luac 破译 + userext::Crypto 链路打通(2026-08-09 深夜,模拟器已关)
### 内存 luac 格式完全破译(s631 = launcher.lua 的 Lua state)
- **s631 段含 launcher.lua 的 luac 缓冲(@0x748,主函数 + 226 常量 + 112 子函数声明)+ 完整字符串池(392 字符串)**
- **TString len 含 \0**(数据 = ln 字节);字段布局 = 标准 Lua 5.1(linedefined/lastlinedefined/nups/numparams/is_vararg/maxstacksize/sizecode)
- launcher.lua.luac 部分提取(主函数 928 指令 + 前 ~20 个子函数);缓冲 0x4fa1 后被堆对象打断
- ComExperienceConfig.lua **完整提取**(1888B,主函数 + 4 子函数)
- **魔改 Lua 字节码:opcode 表重排**(LOADK=34,GETGLOBAL≈20 等,非标准 1/5);指令字段仍 6/8/9/9
- 字符串池关键串:`userext` + `Crypto` + `getStringFromFile` + `X1V5fzTo` + `encryptString` + `string` + `open` + `write` + `close` = launcher 的 UDID 文件加解密工具

### userext::Crypto = 资产加解密核心(C++ 绑定)
- 字符串 @0xd08338-0xd083f0:decryptStringWithKeyLua / encryptStringWithKeyLua / encryptXTEA / MD5FileCommon / encryptStringLua / decryptStringLua / decryptXTEA / encryptXTEALua / encodingBase64Lua / decryptXXTEALua
- 注册 @0x40cf7c:decryptStringWithKeyLua→**0x4095b0**, encryptStringWithKeyLua→**0x408ddc**, encryptXTEA→0x3fc774, MD5FileCommon→0x408fcc
- 绑定 → 0x3e7xxx 封装 → **0x8ab25c(decrypt)/0x8ab318(encrypt)** → XXTEAUtil
- **命名反转确认:decryptStringWithKeyLua 用 add 循环(0x8ab094),encryptStringWithKeyLua 用 sub 循环(0x8aaeac)!** 即游戏的"加密"=标准解密运算,"解密"=标准加密运算
- 0x8ab094 的 target=(52/n)*DELTA+0xB54CDA56 非 DELTA 整数倍 → **疑似诱饵/反调试**(实际运行会死循环)
- XXTEAUtil 默认 key = 6bb4c7d132b432820cc35d8e6cc76c6b(count1=16, setter @0x3dabac)
- **KEY1 用 sub/add 循环都解不开资产文件 → 资产 key = Lua 层传入(userext.Crypto.decryptStringWithKeyLua(str, key) 的第二参数)**

### 下一步(最优)
1. **找到 Lua 层调用 userext.Crypto 的 key**(唯一剩余问题):UDID 加密函数 = launcher.lua 子函数[2](常量 userext/Crypto/MD5/X1V5fzTo/encryptString/io.open wb,code=58,无 key 常量 → key 可能是参数/外部传入/默认 KEY1)
2. 修复 launcher.lua 0x4fa1 解析错位 → 完整 112 个子函数 → 找资产加密调用点
3. 魔改 opcode 完整映射(LOADK=34, GETGLOBAL=20 已确认;从 14 个 luac 差分)→ 反编译子函数[2] 确认 encryptString 调用参数
4. 模拟器重启后拉 APK assets(launcher.lua 可能明文)
5. 拿到 key 后用 add 循环(标准加密逻辑)解密资产 = [数据字 + 长度字] 格式

### 本轮工具链(全部可用,离线)
- extract_launcher.py / extract_launcher2.py: 内存 luac 提取器(TString len 含\0,标准字段)
- luac_disasm.py: Lua 5.1 反汇编(标准 opcode,魔改需映射)
- extract_comconfig.py: ComExperienceConfig.lua 完整提取
- find_crypto_lua_reg.py / opcode_probe.py: userext::Crypto 注册表 / opcode 差分
- xxtea_*: XXTEA 解密测试套件(sub/add 循环)

## 五、下一步选项
1. **深挖 VM 指令集**(多小时静态 RE, 纯离线)
2. **新 MuMu 实例 + 完整抓取**(拿全部脚本)
3. 常量级 mod(不反编译, 直接改内存常量——但应用需运行时 patch, 有封号风险)
