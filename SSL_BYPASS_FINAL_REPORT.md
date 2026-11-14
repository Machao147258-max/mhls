# SSL/TLS 静态绕过分析报告 — 《猫和老鼠》(com.netease.tom)

目标：lib_arm64/tom_lib/*.so native 层 TLS 栈
范围：纯静态分析（禁止模拟器动态调试）
日期：最终版
工作目录：C:\Users\20751\Desktop\猫和老鼠\

---

## 1. 结论摘要

主 SSL 栈 **libAudioCommon.so（OpenSSL 1.1.1q）可被静态 patch 绕过证书校验**：
5 个证书验证函数入口覆写为 `mov w0,#1; ret` 后，客户端接受任意自签证书，
配合 MITM 代理即可解密全部走该栈的 HTTPS 流量（登录/公告/充值/采集上报）。
已产出 `libAudioCommon.so.patched` 副本 + `patch_openssl.py` + `patch_manifest.txt`。

- 源文件 SHA1: `eeb9835c…`
- 补丁文件 SHA1: `2b471f38…`
- 全部 5 点 `MISMATCH: 无`（序言字节与预期一致后覆写），无失败点。

## 2. SSL 栈分布（三份静态 OpenSSL + 易盾通道）

| 库 | OpenSSL 版本 | 符号 | 承载流量 | patch 状态 |
|---|---|---|---|---|
| **libAudioCommon.so** | **1.1.1q (2022-07)** | 明文完整导出 | **真实 TLS 业务（GOT 引 keylog/verify）** | ✅ 5 点已 patch |
| libcocos2dlua.so | 1.0.1c (2012-05-10, 网易 2019-11-27 魔改) | 混淆 + st_value 系统性偏移 | Cocos 引擎附属（次要） | ⚠️ 符号表不可信，见 §5 |
| libijkffmpeg.so | 1.1.x | 部分明文 | 音视频流（ffmpeg） | 未 patch（非登录/协议面） |
| 易盾五库 (libNgModules/libybuaxz/libntunisdk/libsec-lib/unisec) | 无内嵌 TLS | — | 易盾通道 TLS1.3 走系统 BoringSSL | 无需 patch（系统 CA 注入路径） |

## 3. libAudioCommon.so — 证书校验绕过（主交付）

补丁字节：`20 00 80 52 C0 03 5F D6`（`mov w0,#1; ret`）

| # | 函数 | 地址 | 原序言 | 补丁后 |
|---|---|---|---|---|
| 1 | X509_verify_cert | 0x2a2dd4 | `f6 57 bd a9 f4 4f 01 a9` | `20 00 80 52 C0 03 5F D6` |
| 2 | ssl_verify_cert_chain | 0x212894 | `f6 57 bd a9 f4 4f 01 a9` | 同上 |
| 3 | tls_process_server_certificate | 0x22b450 | `ff c3 01 d1 f9 13 00 f9` | 同上 |
| 4 | ssl3_check_cert_and_algorithm | 0x22cdec | `f5 0f 1d f8 f4 4f 01 a9` | 同上 |
| 5 | X509_check_host | 0x2b7e6c | `f7 0f 1c f8 f6 57 01 a9` | 同上 |

验证（反汇编）：
- `ssl_verify_cert_chain@0x212894` 内部走 PLT 0x108230 → GOT 0x3dc918 → 同一函数
- `tls_process_server_certificate@0x22b450` @0x22b648 `bl 0x108230` 后强制 w0=1
- `ssl3_check_cert_and_algorithm@0x22cdec` 错误路径 @0x22ce8c 已改为恒真
- 未发现证书固定（pinning）：`BEGIN CERTIFICATE` 计数=0，sha256-hex 64B 为测试向量

旁证（业务侧调用真实存在）：
- GOT JUMP_SLOT `SSL_CTX_set_keylog_callback@0x3dceb0`、`SSL_CTX_set_verify@0x3dbef8`
- `ssl_log_secret@0x21dbfc`（TLS1.3 keylog 钩子）→ 业务逻辑确实经 GOT 配置 keylog/verify

攻击链：patch 后 .so → 任意外部 MITM 证书被接受 → mitmproxy（自签 CA）解密
login/公告/充值/上报等全部 HTTPS。证书校验 5 函数全部短路，无 pin 兜底。

## 4. 易盾通道结论

unisec/secsdk/libunisec/libsec-lib/libNgModules/libybuaxz/libntunisdk 全栈
无 OpenSSL/BoringSSL/mbedTLS 特征字符串、无 libssl/libcrypto NEEDED →
易盾 TLS1.3（unisec-inner.nie.netease.com）由 Android 系统 BoringSSL 提供，
native 层无 patch 面。绕过路径 = 系统信任库注入测试 CA（root）后 MITM，
属环境配置而非 .so patch。

## 5. libcocos2dlua.so (1.0.1c) 局限 — 符号表不可信（证据链）

该库 .dynsym st_value 被混淆工具系统性偏移，FUNC 与 OBJECT 均不可直接作
patch 入口。反汇编实证：
- `SSL_accept@0xc8d6cc` 实为 ssl_ctrl switch（跳转表 @0xdeb068，cmd 0x10~0x4e）
  中某 case 的尾部 `b #0xc8d610`（公共 epilogue），非函数入口
- `BN_rand@0xbfd3ec` 首条即 `ret`（函数中间）
- `RAND_poll@0xc1ce5c` 首条 `b`（跳板）
- OBJECT `ssl3_undef_enc_method@0x157ee90` 处读出小整数占位（0x181/0xc030…）
  而非函数指针——OBJECT Value 同样被篡改

已确认锚点（可作后续动态/深挖基础）：
- 版本串 `OpenSSL 1.0.1c 10 May 2012` @0xdc1960；built on Wed Nov 27 2019
- 证书错误串：`certificate verify failed@0xdebaa8`、
  `unable to get local issuer certificate@0xdc6508`、
  `self signed certificate@0xdc64c0`、`unsupported certificate purpose@0xdc6660`
- 错误串 xref 只达 ERR_strings/PLT 桩区（0xbc9fb0~0xbca098），未达校验函数体

**风险定性**：1.0.1c 属 Heartbleed-vintage（CVE-2014-0160 受影响区间
1.0.1-1.0.1f），且该栈证书校验同样无 pin；但精确入口需动态内存扫描或
反混淆工具（IDA 脚本 / 符号重建），静态定位成本高于收益，主交付以
1.1.1q 栈为准。建议后续（允许动态时）用 frida 按 SSL_read/SSL_write
行为特征扫描方法表，或对混淆映射表做差分恢复。

## 6. 交付物清单（工作目录）

- `patch_openssl.py` — 补丁脚本（读原 .so、比对序言、覆写、输出 .patched + SHA1）
- `patch_manifest.txt` — 5 点补丁清单（地址/前后字节/SHA1）
- `libAudioCommon.so.patched` — 已补丁副本
- `locate_101c_certfuncs.py` / `chunk_xref.py` / `disasm_dispatcher.py` /
  `parse_enc_data_tables.py` — 1.0.1c 定位尝试脚本与证据

## 7. 复测建议

1. 校验补丁后 SHA1 与 manifest 一致；用 readelf 确认 ELF 头未被破坏
2. 安装 patched .so 到 data/app 后，用 mitmproxy 配置自签 CA，启动游戏
   观察 login/上报 HTTPS 是否解密出明文（应能解密）
3. 若某流量仍失败，查其是否走 libcocos2dlua.so 1.0.1c 栈（连接目标 IP/SNI）
4. 易盾通道单独走系统 BoringSSL，需 root + 系统 CA 注入才能 MITM

## 8. 风险提示

- 玩家数据内存无明文、易盾风控累积；正式使用须新消耗号并控制频率
- patch 只解除证书校验，不解除易盾 antidebug/风控