---
name: opencli
description: OpenCLI命令行工具集成 - 将任何网站、Electron应用或本地工具转换为命令行界面。支持66+平台（中国：B站、知乎、小红书、微博等；国际：Twitter、Reddit、HackerNews等）和桌面应用控制（Cursor、ChatGPT、Notion等）。当用户需要：抓取社交媒体数据（评论、热榜、搜索结果）、获取平台热门内容、控制桌面应用、执行自动化CLI操作、获取结构化JSON/CSV数据、或任何涉及浏览器自动化的任务时使用此skill。此skill具备记忆和自我迭代功能，能记住用户偏好、学习工作流、记录问题并持续优化。
---

# OpenCLI v2.3

通用浏览器自动化工具，通过MCP（Model Context Protocol）工具控制浏览器访问各类网站，获取结构化数据。**具备记忆和自我迭代能力，支持自动降级和增强诊断**。

## ⚠️ 重要说明

**本skill提供真正的CLI命令** `opencli`，同时支持MCP工具：

### CLI命令
```bash
opencli doctor                    # 运行诊断检查
opencli fallback <platform>       # 查看降级指南
opencli memory <action>           # 记忆系统管理
opencli iteration <action>       # 迭代引擎管理
opencli reporter <action>         # 任务报告生成
opencli --version                # 显示版本
opencli --help                   # 显示帮助
```

### MCP工具
1. **Chrome DevTools MCP** - 主要工具，直接控制Chrome浏览器
2. **Agent Browser MCP** - 轻量级替代方案
3. **Playwright MCP** - 跨浏览器支持

### 数据抓取工作流

```bash
# 1. 使用 Chrome DevTools MCP 导航到目标页面
chrome-devtools navigate_page url="https://www.xiaohongshu.com/search_result?keyword=卡塔尔旅游"

# 2. 获取页面快照
chrome-devtools take_snapshot

# 3. 点击帖子或执行其他交互
chrome-devtools click uid="xxx"

# 4. 使用其他MCP工具进行截图、数据提取等
```

---

## 🔍 增强诊断系统

### doctor 命令
```bash
# CLI方式（推荐）
opencli doctor

# JSON格式输出
opencli doctor --json

# Python脚本方式
python scripts/opencli.py doctor
python scripts/diagnostic.py --json
```

**诊断项目**：
- ✅ Chrome浏览器安装状态（跨平台自动检测）
- ✅ Browser Bridge扩展连接状态
- ✅ Node.js环境
- ✅ 网络连接状态
- ✅ 各平台可达性

**输出示例**：
```
========================================================
🔍 OpenCLI 诊断报告
========================================================
时间: 2026-03-30T12:00:00

📊 摘要: 5 ✅ | 2 ⚠️ | 1 ❌

✅ Chrome浏览器
   已安装: C:\Program Files\Google\Chrome\Application\chrome.exe

⚠️ Browser Bridge扩展
   请手动确认扩展已启用
```

---

## 🔄 自动降级机制

当首选工具不可用时，自动提供替代方案：

```bash
# 查看特定平台的降级指南
python scripts/fallback_manager.py xiaohongshu

# 查看降级统计
python scripts/fallback_manager.py xiaohongshu stats

# 检查扩展状态
python scripts/fallback_manager.py xiaohongshu status
```

### 平台反爬强度评估

| 反爬等级 | 平台示例 | 推荐工具 |
|---------|---------|---------|
| 🔵 低 | HackerNews, Reddit | Agent-browser |
| 🟡 中 | Twitter, YouTube | Playwright |
| 🔴 高 | 小红书, B站, 知乎, 微博 | Chrome DevTools |
| ⚫ 极高 | 微信 | 手动操作 |

### 备用工具选择

| 工具 | 适用场景 | Token效率 |
|------|---------|----------|
| **Chrome DevTools** | 高反爬网站、调试 | ⭐⭐⭐ |
| **Playwright** | 跨浏览器测试 | ⭐⭐⭐⭐ |
| **Agent-browser** | 简单自动化 | ⭐⭐⭐⭐⭐ |

---

## 记忆系统

自动记录操作历史、用户偏好，知识库，让工具越用越懂你。

### 会话记忆
- 自动记录每次命令执行
- 包含：命令、平台、结果、状态

### 用户偏好
- 常用平台、默认格式、输出目录
- 跨会话持久化

### 知识库
- 记录已抓取的数据摘要
- 平台使用统计

### 记忆脚本
```bash
python scripts/memory_manager.py status                    # 查看记忆状态
python scripts/memory_manager.py history                   # 查看会话历史
python scripts/memory_manager.py get-prefs                 # 获取用户偏好
python scripts/memory_manager.py query <关键词>            # 查询知识库
python scripts/memory_manager.py clear-session              # 清空会话记忆
```

---

## 迭代引擎

问题追踪、改进建议，工作流学习、报告生成。

### 问题管理
```bash
# 报告问题
python scripts/iteration_engine.py report-problem <平台> <命令> <错误信息> [优先级]

# 查看问题
python scripts/iteration_engine.py list-problems [状态] [平台]

# 更新状态
python scripts/iteration_engine.py update-status <id> <状态> [解决方案]
```

### 生成报告
```bash
python scripts/iteration_engine.py generate-report
```

---

## 🎯 主动报告机制（核心规则）

**每次任务完成后，Agent 必须主动生成任务报告，无需用户询问。**

### 报告生成规则

```
当任务完成时（包括成功完成、部分完成、遇到问题）：
  │
  ├─ 1️⃣ 生成任务报告
  │     ├─ 完成情况：哪些做完了，哪些没做完
  │     ├─ 数据统计：抓取了多少条数据
  │     ├─ 遇到的问题：技术问题、工具限制、预期差异
  │     └─ 原因分析：为什么出问题，哪里设计不足
  │
  ├─ 2️⃣ 给出迭代方案
  │     ├─ 短期改进：本次发现的问题如何修复
  │     ├─ 中期改进：skill需要增加什么能力
  │     └─ 长期改进：架构层面的优化建议
  │
  ├─ 3️⃣ 询问用户
  │     └─ "需要我升级迭代吗？允许后立即执行"
  │
  └─ 4️⃣ 等待用户响应
        ├─ 允许 → 执行升级，修改skill文件，推送到GitHub
        └─ 拒绝 → 记录报告到 iteration/reports/ 待处理
```

### 任务报告脚本
```bash
# 创建报告
python scripts/task_reporter.py create <任务名> <描述>

# 查看待处理报告
python scripts/task_reporter.py pending

# 标记为已完成
python scripts/task_reporter.py complete <报告ID>
```

---

## 数据存储

```
~/.config/opencode/skills/opencli/data/
├── memory/
│   ├── session-memory.json     # 会话记忆
│   ├── user-preferences.yaml  # 用户偏好
│   └── knowledge-base.md      # 知识库
├── iteration/
│   ├── problems.json          # 问题记录
│   ├── improvements.md        # 改进建议
│   ├── workflows.yaml         # 学习的工作流
│   └── reports/              # 迭代报告
├── fallback_log.json         # 降级事件日志
└── outputs/                  # 下载的文件
```

### 自定义数据目录

可以通过环境变量自定义数据目录：
```bash
# Linux/macOS
export OPENCLI_DATA_DIR="/path/to/data"

# Windows
set OPENCLI_DATA_DIR=C:\path\to\data
```

---

## 前置条件

1. Chrome浏览器已安装并打开
2. Browser Bridge扩展已启用（可选）

```bash
# 详细诊断（推荐）
python scripts/diagnostic.py
```

---

## 平台速查

| 平台 | 反爬等级 | 推荐工具 | 备注 |
|------|---------|---------|------|
| B站 | 🔴 高 | Chrome DevTools | 需登录态 |
| 知乎 | 🔴 高 | Chrome DevTools | 需登录态 |
| 小红书 | 🔴 高 | Chrome DevTools | 需登录态 |
| 微博 | 🔴 高 | Chrome DevTools | 需登录态 |
| Twitter | 🟡 中 | Playwright | API限制 |
| Reddit | 🔵 低 | Agent-browser | 直接可访问 |
| HN | 🔵 低 | Agent-browser | 直接可访问 |
| 桌面应用 | - | Agent-browser | Electron |

---

## MCP工具参考

### Chrome DevTools MCP
```bash
chrome-devtools navigate_page url="https://..."    # 导航
chrome-devtools take_snapshot                      # 获取快照
chrome-devtools click uid="xxx"                   # 点击元素
chrome-devtools fill uid="xxx" value="..."        # 填写表单
chrome-devtools take_screenshot                    # 截图
```

### Agent Browser MCP
```bash
navigate url="https://..."                         # 导航
snapshot                                           # 获取快照
click ref="@e1"                                    # 使用引用点击
```

完整命令列表见 [references/commands.md](references/commands.md)

---

## 故障排查

| 问题 | 解决 |
|------|------|
| 扩展未连接 | 使用 `python scripts/diagnostic.py` 详细诊断 |
| 返回空数据 | 使用 `python scripts/fallback_manager.py <平台>` 查看备用方案 |
| 执行失败 | 检查chrome扩展状态，或使用chrome-devtools直接操作 |
| 高反爬网站 | 使用Chrome DevTools MCP作为主要工具 |

---

## 更新日志

### v2.4 (2026-03-30)
- ✅ 新增单元测试框架 (tests/)
- ✅ 新增config.yaml配置文件支持
- ✅ 新增GitHub Actions CI/CD
- ✅ 配置类支持YAML配置读取

### v2.3 (2026-03-30)
- ✅ 新增日志系统 (shared/logger.py)
- ✅ 实现真正的CLI命令 (opencli.py)
- ✅ 修复所有P2类型注解问题
- ✅ 清理urllib导入到文件顶部
- ✅ 清理注释中的Unix路径

### v2.2 (2026-03-30)
- ✅ 修复硬编码路径问题，使用跨平台配置模块
- ✅ 修复subprocess跨平台兼容性问题
- ✅ 修复Windows彩色输出兼容性问题
- ✅ 网络检测改用Python urllib，替代curl命令

### v2.1 (2026-03-29)
- ✅ 新增主动报告机制
- ✅ 新增任务报告生成器

### v2.0 (2026-03-29)
- ✅ 新增增强诊断系统
- ✅ 新增自动降级机制
- ✅ 新增记忆系统
- ✅ 新增迭代引擎

---

## 参考文档

- 命令参考：[references/commands.md](references/commands.md)
- 记忆系统：[scripts/memory_manager.py](scripts/memory_manager.py)
- 迭代引擎：[scripts/iteration_engine.py](scripts/iteration_engine.py)
- 增强诊断：[scripts/diagnostic.py](scripts/diagnostic.py)
- 自动降级：[scripts/fallback_manager.py](scripts/fallback_manager.py)
- 任务报告：[scripts/task_reporter.py](scripts/task_reporter.py)
- 共享配置：[scripts/shared/config.py](scripts/shared/config.py)
