# OpenCLI Skill

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
opencli <command> -f table    # 表格（默认）
```

## 平台支持

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

## 前置条件

1. Chrome浏览器已安装并打开
2. Browser Bridge扩展已启用

```bash
opencli doctor  # 检查连接状态
```

## 故障排查

| 问题 | 解决 |
|------|------|
| 扩展未连接 | `opencli doctor`检查，激活Chrome扩展 |
| 返回空数据 | 确保Chrome已登录目标网站 |
| 执行失败 | 查看迭代报告获取详情 |

## 文件结构

```
opencli-skill/
├── SKILL.md                    # 主技能文档
├── references/
│   └── commands.md             # 命令参考
├── scripts/
│   ├── memory_manager.py       # 记忆系统
│   └── iteration_engine.py    # 迭代引擎
└── data/                      # 数据存储（用户数据）
    ├── memory/
    ├── iteration/
    └── outputs/
```

## 安装

将整个文件夹复制到 OpenCode 的 skills 目录：

```bash
# Windows
cp -r opencli-skill ~/.config/opencode/skills/

# 或在 OpenCode 中使用 skill-creator
```

## License

MIT