---
name: opencli
description: OpenCLI命令行工具集成 - 将任何网站、Electron应用或本地工具转换为命令行界面。支持66+平台（中国：B站、知乎、小红书、微博等；国际：Twitter、Reddit、HackerNews等）和桌面应用控制（Cursor、ChatGPT、Notion等）。当用户需要：抓取社交媒体数据（评论、热榜、搜索结果）、获取平台热门内容、控制桌面应用、执行自动化CLI操作、获取结构化JSON/CSV数据、或任何涉及浏览器自动化的任务时使用此skill。此skill具备记忆和自我迭代功能，能记住用户偏好、学习工作流、记录问题并持续优化。
---

# OpenCLI

通用CLI工具，通过预置适配器控制浏览器访问各类网站，获取结构化数据。**具备记忆和自我迭代能力**。

## 核心能力

### 1. 数据抓取
```bash
opencli bilibili hot --limit 10          # B站热搜
opencli zhihu hot -f json                # 知乎热榜
opencli hackernews top                   # HN热门
opencli reddit hot                       # Reddit热门
opencli twitter trending                 # Twitter趋势
```

### 2. 评论抓取
```bash
opencli bilibili comments <bvid> --limit 20   # B站评论
```

### 3. 内容下载
```bash
opencli bilibili download <bvid>              # 视频（需yt-dlp）
opencli zhihu download <url>                  # 文章为Markdown
opencli xiaohongshu download <note_id>       # 图片/视频
```

### 4. 输出格式
```bash
opencli <command> -f json     # JSON（程序处理）
opencli <command> -f yaml     # YAML
opencli <command> -f csv      # CSV
opencli <command> -f table     # 表格（默认）
```

---

## 记忆系统

自动记录操作历史、用户偏好，知识库，让工具越用越懂你。

### 会话记忆
- 自动记录每次命令执行
- 包含：命令、平台、结果、状态
- 存储：`session-memory.json`

### 用户偏好
- 常用平台、默认格式、输出目录
- 跨会话持久化
- 存储：`user-preferences.yaml`

### 知识库
- 记录已抓取的数据摘要
- 平台使用统计
- 存储：`knowledge-base.md`

### 记忆脚本
```bash
python scripts/memory_manager.py status                    # 查看记忆状态
python scripts/memory_manager.py history                  # 查看会话历史
python scripts/memory_manager.py get-prefs               # 获取用户偏好
python scripts/memory_manager.py query <关键词>          # 查询知识库
python scripts/memory_manager.py clear-session           # 清空会话记忆
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

### 工作流学习
```bash
# 学习工作流
python scripts/iteration_engine.py learn-workflow <名称> <步骤JSON> <平台列表>

# 查看工作流
python scripts/iteration_engine.py list-workflows [平台]
```

### 生成报告
```bash
python scripts/iteration_engine.py generate-report
# 生成迭代报告，包含：执行摘要、问题统计、改进建议、下一步行动
```

---

## 完整工作流

### 执行任务
1. 用户提出需求（如：抓取B站热门评论）
2. 执行opencli命令
3. **自动记录**：记忆系统保存操作，知识库更新统计

### 遇到问题
1. 执行失败 → **自动报告问题**到迭代引擎
2. 迭代引擎生成改进建议
3. 任务结束时 **生成迭代报告**

### 持续优化
1. 查看报告 → 了解问题和建议
2. 处理问题 → 更新问题状态
3. 学习新工作流 → 提高效率

---

## 数据存储

```
~/.config/opencode/skills/opencli/data/
├── memory/
│   ├── session-memory.json     # 会话记忆
│   ├── user-preferences.yaml   # 用户偏好
│   └── knowledge-base.md      # 知识库
├── iteration/
│   ├── problems.json          # 问题记录
│   ├── improvements.md        # 改进建议
│   ├── workflows.yaml        # 学习的工作流
│   └── reports/              # 迭代报告
└── outputs/                  # 下载的文件
```

---

## 前置条件

1. Chrome浏览器已安装并打开
2. Browser Bridge扩展已启用

```bash
opencli doctor  # 检查连接状态
```

---

## 平台速查

| 平台 | 命令前缀 | 说明 |
|------|----------|------|
| B站 | `bilibili` | 热榜、评论、下载 |
| 知乎 | `zhihu` | 热榜、搜索、文章 |
| 小红书 | `xiaohongshu` | 搜索、feed、下载 |
| 微博 | `weibo` | 热搜 |
| Twitter | `twitter` | 趋势、发推 |
| Reddit | `reddit` | 热门、搜索 |
| HN | `hackernews` | top、new、best |
| 桌面应用 | `cursor`, `chatgpt`, `notion` | 应用控制 |

完整命令列表见 [references/commands.md](references/commands.md)

---

## 故障排查

| 问题 | 解决 |
|------|------|
| 扩展未连接 | `opencli doctor`检查，激活Chrome扩展 |
| 返回空数据 | 确保Chrome已登录目标网站 |
| 执行失败 | 查看迭代报告获取详情 |

---

## 参考文档

- 命令参考：[references/commands.md](references/commands.md)
- 记忆系统：[scripts/memory_manager.py](scripts/memory_manager.py)
- 迭代引擎：[scripts/iteration_engine.py](scripts/iteration_engine.py)