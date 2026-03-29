# OpenCLI Skill v2.1

通用CLI工具，通过预置适配器控制浏览器访问各类网站，获取结构化数据。**支持自动降级、增强诊断和主动报告机制**。

## ✨ 核心功能

### 主动报告机制（v2.1新增）
**每次任务完成后自动生成报告，无需用户询问**
- 完成情况总结
- 数据统计
- 遇到的问题
- 迭代方案建议
- 自动询问用户是否升级

### 诊断与降级
```bash
# 详细诊断
python scripts/diagnostic.py

# 查看平台降级指南
python scripts/fallback_manager.py xiaohongshu

# 生成任务报告
python scripts/task_reporter.py generate
```

## 平台支持

| 平台 | 反爬等级 | 推荐工具 |
|------|---------|---------|
| 🇨🇳 小红书 | 🔴 高 | Chrome DevTools |
| 🇨🇳 B站 | 🔴 高 | Chrome DevTools |
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
    ├── task_reporter.py       # 主动报告机制 (v2.1)
    ├── diagnostic.py           # 增强诊断系统
    ├── fallback_manager.py     # 自动降级管理器
    ├── memory_manager.py       # 记忆系统
    └── iteration_engine.py     # 迭代引擎
```

## 安装

```bash
cp -r opencli-skill ~/.config/opencode/skills/
```

## License

MIT