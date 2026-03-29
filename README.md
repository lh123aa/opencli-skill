# OpenCLI Skill v2.0

通用CLI工具，通过预置适配器控制浏览器访问各类网站，获取结构化数据。**支持自动降级和增强诊断**。

## ✨ 新功能 (v2.0)

- 🔍 **增强诊断系统** - 详细检查连接状态，提供修复建议
- 🔄 **自动降级机制** - 扩展不可用时自动推荐备用工具
- 🇨🇳 **中国平台增强** - 小红书、B站、知乎、微博专用指南

## 核心能力

### 数据抓取
```bash
opencli bilibili hot --limit 10          # B站热搜
opencli xiaohongshu search <关键词>      # 小红书搜索
opencli hackernews top                   # HN热门
```

### 诊断与降级
```bash
# 详细诊断
python scripts/diagnostic.py

# 查看平台降级指南
python scripts/fallback_manager.py xiaohongshu
```

## 平台支持

| 平台 | 反爬等级 | 推荐工具 |
|------|---------|---------|
| 🇨🇳 小红书 | 🔴 高 | Chrome DevTools |
| 🇨🇳 B站 | 🔴 高 | Chrome DevTools |
| 🇨🇳 知乎 | 🔴 高 | Chrome DevTools |
| 🐦 Twitter | 🟡 中 | Playwright |
| 🔵 Reddit | 🔵 低 | Agent-browser |

## 文件结构

```
opencli-skill/
├── SKILL.md                    # 主技能文档
├── README.md
├── references/
│   └── commands.md             # 命令参考（含中国平台指南）
└── scripts/
    ├── diagnostic.py          # 增强诊断系统
    ├── fallback_manager.py    # 自动降级管理器
    ├── memory_manager.py      # 记忆系统
    └── iteration_engine.py    # 迭代引擎
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