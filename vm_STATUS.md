# 猫和老鼠 魔改 Lua VM 逆向状态 (2025-07 更新)

## ✅ 已破解:魔改 Lua 5.1 VM 指令集

### 文件版本
- **新版 APK**(混淆壳 libcocos2dlua.so_RUNTIME.so, 25,179,584B):当前模拟器运行版本
- 内存 luac(undump 后)= 32 位标准小端指令,opcode = 低 6 位
- 旧版(25,990,592B)的 0x66606c = 另一套字节码解释器(非 luac VM)

### VM 结构(新版, 混淆壳内)
| 组件 | 地址 (RUNTIME so 文件偏移) |
| --- | --- |
| luaV_execute 入口 | 0x609098 |
| 主循环取指 | 0x6091d4: `ldr w4,[x27]` + `and w19,w4,#0x3f` |
| A 字段 | `ubfx x7,x4,#6,#8` (bits 6-13) |
| B 字段 | bits 14-22 (9位) |
| C 字段 | bits 23-31 (9位) |
| Bx 字段 | bits 14-31 (18位) |
| sBx | Bx - 131071 |
| **格式表** | **0xcd3820** (42 字节, 低2位=模式: 0=ABC 1=ABx 2=AsBx) |
| 跳转表 | 0xcd2c84 (op3-37, 2字节有符号偏移×4, 基准 0x6092a0) |

### 常量表 (标准 TValue 编码, 在 luac 内)
- 位置: code 后 `sizek` 字段
- 类型: 0=nil 1=bool 3=double(8B) 4=string(长度字+内容)
- **索引 = Bx - 256**(LOADK 直接索引;SETTABLEK 的 B/C 为 256+k)
- 内存格式注意: 常量区可能被下一块截断(解析时容错, 见 pseudo_gen.py)

## ✅ 已确认 opcode (21/42)

| op | 语义 | 操作数 | 备注 |
| --- | --- | --- | --- |
| 2 | TESTSET | R[A]=R[B] if R[B]~=nil else pc+=C | `local x = a or 20` 模式 |
| 4 | CALL | 调用 | B=参数数 C=结果数 |
| 5 | RETURN | R[A..] C-1 个值 | C=数量+1 (C=1 无值) |
| 6 | FORLOOP? | sBx | 循环跳 |
| 7 | MOVE | R[A] <- R[C] | B 未用 |
| 8 | FORPREP? | sBx | 循环跳 |
| 9 | CALLSETUP | 调用前准备 | C=参数数标记 |
| 10 | LOADIMM | R[A] <- Bx 整数 | 小整数优化 |
| 14 | TEST | 测试 R[A] | 条件 |
| 17 | GETTABLE | R[A] <- R[C][B] | **B=键 C=表 (与标准交换!)** |
| 18 | CONCAT? | R[A] <- R[B..C] | 范围拼接 |
| 20 | LOADK | R[A] <- k[Bx] | 常量 |
| 21 | JMP | pc += sBx | 短跳 |
| 22 | EQ | 比较 R[B]==R[C] | 条件 |
| 23 | FORLOOP2 | 循环条件更新+测试 | 配合 JMP |
| 25 | GETTABLE2 | 同 GETTABLE | 变体 |
| 28 | LOADNIL? | 清寄存器 | 函数头初始化 |
| 30 | NEWTABLE | R[A] <- {}(容量 B) | B=元素数 |
| 31 | LOADNIL2? | 清寄存器 | |
| 33 | SELF | R[A] <- R[C]:method(B) | B=方法名常量 |
| 34 | GETGLOBAL | R[A] <- global[k[Bx]] | |
| 35 | ARITH | R[A] <- R[B] op R[C] | 二元算术 |
| 36 | SETTABLEK/LOADK2 | R[A][k[C-256]] <- R[B]/k[B] | **C>=256 时 = 常量索引 k[C-256] (已实测: 005 的 C=283→'ctor', 284→'init' 递增吻合!); B=值** |

**关键规律: 表操作 B/C 交换**(GETTABLE: B=键 C=表; SETTABLEK: B=值 C=键)

## ✅ 读取成果 (vm_out/)

| 文件 | 内容 |
| --- | --- |
| src_catchGame_data_role.lua.asm | 13436 条 (纯配置数据表) |
| src_catchGame_systems_GmSystem.lua.lua_pseudo | GM 命令/网络协议可读! |
| src_catchGame_systems_SquareSystem.lua.lua_pseudo | 18 个函数, 逻辑清晰 |
| src_catchGame_box2d_RubeSceneReader.lua.lua_pseudo | 场景读取器 |
| src_catchGame_systems_UGCSystem.lua.lua_pseudo | require 列表+常量全明文 |
| ... | 共 12 个脚本 × (asm + pseudo) |

### 示例 (GmSystem 反编译效果)
```lua
TJNetMgr:regMsgHandler(NetMsg.CS_CMD_FRIEND_GET_NETEASE_FRIEND, self.onGetNeteaseFriend)
TJNetMgr:regMsgHandler(NetMsg.CS_CMD_VANGUARD_SCORE_NTF, self.onNtfPioneerScore)
TJNetMgr:regMsgHandler(NetMsg.CS_NTF_GM_ACCOUNT, self.setGMAccount)

function GmSystem:setFraudReport(a, b, c, d)
  local msg = { type = NetGameEnum.E_DEBUG_TYPE.E_DEBUG_TYPE_SET_FRAUD_REPORT_INFO,
                setFraudReport = { beReportedCount=a, fraudValue=b, ... } }
  TJNetMgr:sendMsg(NetMsg.CS_CMD_DEBUG, msg)
end

## ✅ 反编译器 v2 (vm_rev_decompiler.py) + REV_OUT/

- 输入: luac 二进制 → 输出: 结构化 Lua(require/class/字段赋值识别!)
- 14 个脚本全部反编译 → `REV_OUT/*.rev.lua` + `_API_REPORT.txt`(模块 API 表面!)
- 已识别: 9 个系统脚本的 require 链 + class 名 + 类方法名序列(如 ModuleManager: ctor/init/initFashionModule/getFileList/parseFileList/getModuleConfig/parseModuleConfig/saveModuleConfig/getReadyModuleFiles/getReadyModuleNames/canDownload)
- 指令格式实测: op6 + A8 + B9(v>>14) + C9(v>>23)(**B/C 与标准 Lua 交换!**)
- 常量索引: LOADK/GETGLOBAL 用 Bx(v>>14, 18位); 表操作 C>=256 时 = k[C-256]
- 数据脚本(000-004): 字段名提取成功(id/bignodeImage/shareImage/interactiveID/hasLockedPop/locktips/lockimg...) — 键值对用 LOADIMM 递增序号 + op36 交替```

## 🟡 剩余工作
1. 剩余 ~21 个 opcode 标注 (算术细分 ADD/SUB/MUL/DIV、SETTABLE、SETGLOBAL、CLOSURE、VARARG、TAILCALL、SETLIST、比较 LT/LE、GETUPVAL/SETUPVAL 等) — 需要复杂业务脚本(进游戏触发战斗/匹配模块)
2. 完整反编译器 (伪代码 → 可编译 Lua 源码)
3. 全量脚本 (40000+ 个, X1V5fzTo 加密)
4. role.lua 等大文件的常量表分离存储问题 (与 .ld 文件关联)

## 🔐 XXTEA 加密破解进度 (重大进展!)
### 已定位 (RUNTIME so 文件偏移)
- 解密包装器: **0x85261c** (读密文 + 16B 密钥)
- 读取器: **0x852548** (memcpy 类)
- 解密核心: **0x8526a8-0x852750** (XXTEA 变体!)
- 相关: 0x852800 (另一加密函数, 0x9e3779b9), 0x8529c8 (异或加密层, cmp w3,#0xf)

### 算法 (从汇编精确重构!)
```
rounds = 6 + 52 // n;  sum 从 rounds*0x9e3779b9 递减 (每轮 sum -= DELTA, 到 0 停)
每轮: e = sum >> 2
  p = n-1..1:  ki = (p ^ e) & 3
    MX = ((z^k[ki]) + (y^sum)) ^ (((y>>3)^(z<<4)) + ((y<<2)^(z>>5)))
    v[p] -= MX;  y = v[p]
  v[0]: ki = e & 3
    MX0 = (((z>>5)^(y<<2)) + ((z<<4)^(y>>3))) ^ ((y^sum) + (z^k[ki]))
    v[0] -= MX0
```
- DELTA = 0x9e3779b9 (标准!); 汇编中 0x61c88647 = -DELTA mod 2^32 (sum 递减实现)
- 密钥 = 16B (4 × uint32, 小端), 由调用者传入 (壳区, 静态不可读)
- 文件格式: `X1V5fzTo` + 4B 0 + XXTEA 密文
- 内存格式: 8B 元数据 (魔数 0x00014001/.ld 或 0x0001a013/.bin + 大端长度) + 同上

### 已确认 (明文, 密文) 黄金对
- common_utils.luac (3574B, parse_end) ↔ 217a71cb4ce1b6a6193f0dabeaa67ff7.bin (3588B)
- 设备 src 缓存: 1703 .bin + 16 .ld

### 未突破
- 密钥本体: 
  - 已实现位级求解器 (xxtea_bitcrack*.py, 单方程单未知 32 位精确解, 5/5 单元测试通过!)
  - 但"已知明文攻击"需要中间态: 解密第1轮输出 ≠ 明文(是中间态!) → 反推出现伪自洽(尾部 0 区弱方程)与真实冲突(非 0 区 p=883 冲突!)
  - 正确路线: 全链联立求解 (6 轮 × n 字, 中间态消元) 或 n=2 小文件单 k 消元 (32 轮)
  - 或动态提取: so 映射读不了 (I/O error), 需要注入类手段 (高风险)
- 密钥源 = 壳区 (0-0x395000 文件密文, 运行时解密)

### 加密/解密函数完整清单 (RUNTIME so 文件偏移)
| 地址 | 功能 |
| --- | --- |
| 0x85261c | 解密包装器 (读密文 + 16B key) |
| 0x8526a8 | XXTEA 解密核心 (sum 从 rounds*DELTA 递减) |
| 0x852548 | 读取器 (memcpy 类) |
| 0x852804 | XXTEA 加密核心 (sum 从 0 递增, z=v[n-1] 固定!非对称!) |
| 0x8529c8 | 加密分发器 (长度≤15: key 截断+0填充) |
| 0x8529cc | 异或层包装 (memcpy key 到 16B 缓冲) |

## 工具
- vm_disasm_engine.py — 反汇编器 (输入 luac → .asm)
- vm_pseudo_gen.py — 伪代码生成器 (输入 luac → .lua_pseudo)
- vm_extract_mega_luac.py — 从内存 dump 提取 luac
- vm_op_stats.py — opcode 行为统计
- crypto_xxtea_*.py — XXTEA 解密/反推工具集 (crypto_xxtea_search.py = 组合搜索!)

## 内存抓取链路 (已实测安全)
dd /proc/PID/mem → mega/all.bin + segs_6894.json → extract_mega_luac.py → 反汇编
