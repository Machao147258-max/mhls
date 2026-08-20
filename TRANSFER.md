# 🐱🐭 猫和老鼠 逆向交接文档 (新对话从这里开始)

> 2025-07 生成 · 读本文件 + `vm_STATUS.md` + **`STATUS.md`(旧会话阶段总结,含 userext::Crypto 链路!)** 即可接力,无需翻旧对话

## ⚠️ 两个 STATUS 文件
- `STATUS.md`(11KB, 2026-08-08/09 旧会话总结):技术栈、X1V5fzTo 加密、**抓取管线(零注入已全通)**、**unisec 反作弊画像**、**内存 luac 破译 + userext::Crypto C++ 加解密核心链路已打通**、CDN 全量拉取成功
- `vm_STATUS.md`(7.6KB, 本会话):VM 指令集 21+ opcode、XXTEA 重构、反编译器 v2
- `tb_tom_*.js`(Frida 脚本):模块枚举(tb_tom_mods 已跑出 350 个 so)、lua 状态探测等 —— 新对话直接复用

## 1. 项目目标(用户原话)

1. 全面逆向游戏(com.netease.tom 猫和老鼠,网易)
2. **Hook 触发角色动作代码**
3. **读取内存**
4. **内存修改不被对方检测**(免反作弊)

## 2. 当前环境(已就绪!)

- 模拟器 MuMu 15 已连:**ADB 127.0.0.1:7555**(root shell `munch:/ #` 可用!)
- 伪装 SM-A5560 / Android 15(ro.product.model=SM-A5560)
- **游戏已在运行:com.netease.tom(pid 1854)**(还有 PushService)
- KernelSU root(可执行 su)
- 保底机 = vm 0(ADB 16416,**不要启动/不要动!**)
- 工具:`D:\MuMuPlayer\nx_main\adb.exe`、`mumu-cli.exe`(控制模拟器)

## 3. 素材位置(本文件夹 + tomdump/)

| 路径 | 内容 |
| --- | --- |
| `C:\Users\20751\tomdump\device_libs\` | RUNTIME so(25,179,584B 壳混淆版)、libcocos2dlua.so、libsecsdk.so(网易安全SDK!) |
| `C:\Users\20751\tomdump\device_src\` | 1703 个加密文件(.bin/.ld,X1V5fzTo 头) |
| `C:\Users\20751\tomdump\mega\all.bin` | 246MB 内存 dump(代码/字符串/数据) |
| `C:\Users\20751\tomdump\ALL_SCRIPTS\` | 14 个内存 luac × (asm 反汇编 + luac 二进制) |
| `REV_OUT\` | 14 个反编译输出 + `_API_REPORT.txt`(模块 API 表面) |
| `vm_out\` | 旧版 12 脚本伪代码(GmSystem/SquareSystem/UGCSystem 可读!) |
| `vm_STATUS.md` | 详细状态(VM 指令集/XXTEA/opcode 表) |
| `vm_rev_decompiler.py` | 反编译器 v2(require/class/字段识别) |
| `vm_disasm_engine.py` / `vm_pseudo_gen.py` / `vm_table_restore.py` | 反汇编/伪代码/表还原工具 |
| `crypto_xxtea_*.py` | XXTEA 工具(bitcrack/z3/dict/debug) |

## 4. 已破解(核心成果)

### 4.1 魔改 Lua 5.1 VM(21+/42 opcode 确认)
- 指令格式:**op6 + A8 + B9(v>>14) + C9(v>>23)**(B/C 与标准 Lua **交换**!)
- Bx = v>>14(18 位);LOADK/GETGLOBAL 用 Bx 索引常量
- 常量表:0=nil 1=bool 3=double(8B) 4=string(4B 长+内容)
- **op36(LOADK2/SETTABLEK):键 = C-256 常量,值 = B 寄存器/常量**(已实测:005 的 C=283→'ctor',284→'init' 方法名递增吻合)
- require/class 模式:9 个系统脚本的模块头已还原(如 ModuleManager 13 方法)
- 关键规律:表操作 B/C 交换(GETTABLE: B=键 C=表;SETTABLEK: B=值 C=键)

### 4.2 XXTEA 变体(完整重构,密钥未破)
```
rounds = 6 + 52//n; DELTA = 0x9e3779b9; sum 加密从 0 递增/解密从 rounds*DELTA 递减
MX = ((z^k)+(y^sum)) ^ ((y>>3^z<<4)+(y<<2^z>>5))   ← 魔改变体
加密 z = v[n-1] 固定(非对称!);解密 z = v[p-1]
密钥索引: ki = (p^e)&3(主循环), e&3(v[0])
文件格式: 'X1V5fzTo' + 4B + XXTEA 密文
黄金对: common_utils(3574B 明文) ↔ 217a71cb4ce1b6a6193f0dabeaa67ff7.bin(3588B)
```
- 密钥源 = 壳区(0-0x395000 文件密文,运行时解密)
- **位级求解器已实现且单测通过**,但需全链中间态(6 轮 × n 字),静态难破
- **暴力已由用户叫停** → 密钥只能动态拿(hook 解密函数 / 抓内存)

### 4.3 内存 dump 已确认的 Hook 线索(RUNTIME so)
```
'runAction'   @ 0xc8e588   ← cocos 动画播放 API(触发动作的候选 hook 点!)
'playAction'  @ 0xc98b80   ← 游戏动作播放
'Animate'     @ 0xc8d9db / 0xc8fea0 / 0x11ab6b / 0x1c3129 / 0x1c4d5c
'Animation'   @ 0x11a46c 等
内存 dump 另有: skill/Skill @ 0x30b6f06 一带(游戏技能代码区!)
```

## 5. 未破解 / 卡点

- ❌ XXTEA 密钥(静态无解,已停暴力;动态:hook 0x85261c 解密包装器即可抓 key!)
- ❌ 003 role.lua 常量表在 .ld 密文里(59da8bd0.ld 269KB,需密钥)
- ❌ 角色动作相关脚本未抓到(已抓 14 个多为配置/系统模块)
- ❌ libsecsdk.so(网易安全 SDK,反作弊)未逆向 ← 免检测的关键
- ❌ 网络协议未分析
- ⚠️ so 映射内存读不了(I/O error,转译层保护)→ 需通过游戏进程 /proc/pid/mem 读

## 6. 下一步执行计划(按优先级)

### P0:Hook 触发角色动作 + 读内存(动态,环境已就绪!)
1. 抓角色动作脚本:游戏在跑(pid 1854)→ dump 其内存找 luac(角色/动画/技能模块)
   - `adb shell su -c 'cat /proc/1854/maps'` 找 anon 段 → 搜 '1b4c7561'(luac 头)
2. Hook 点:确认 runAction(0xc8e588)/playAction(0xc98b80)的函数地址(ELF 段表 xref)
3. 装 frida-server(KernelSU su 下跑)→ hook 动画函数 → 强制触发角色动作
4. 读内存:frida Memory.read* / /proc/pid/mem

### P1:动态拿 XXTEA 密钥
- hook 0x85261c(解密包装器)的参数 3(16B key)即可(需先定位运行时基址)
- 或 /proc/pid/mem 搜壳区解密后的 key(16B 连续)

### P2:免检测(libsecsdk)
- 逆向 libsecsdk.so(字符串/导出表)→ 找检测点(hook 篡改/上报)
- 内存修改免检测 = hook 掉完整性校验/上报

## 7. 工具速查

```bash
ADB=D:\\MuMuPlayer\\nx_main\\adb.exe
$ADB -s 127.0.0.1:7555 shell su -c '...'   # root 命令
$ADB -s 127.0.0.1:7555 shell "ps -A | grep tom"  # 游戏 pid
# 反编译: python rev_decompiler.py <luac>
# 反汇编: python disasm_engine.py <luac>
# 表还原: python table_restore.py <luac>
```

## 8. 会话教训(重要!)

- 用户强调**逆向为主**,暴力攻击(字典/Z3)已叫停—— 密钥走动态
- **保底机(vm 0, 16416)不要启动**
- 每次成果同步到本文件夹(REV_OUT/ALL_SCRIPTS/工具)
- XXTEA 反推易出"伪自洽"(尾部 0 弱方程),验证必须用非 0 明文区
