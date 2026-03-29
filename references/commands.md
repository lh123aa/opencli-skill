# OpenCLI 命令参考 v2.0

## 基础命令

```bash
opencli --version              # 查看版本
opencli doctor                 # 诊断连接状态
opencli list                  # 列出所有命令
opencli list -f json          # JSON格式列出命令
```

## 输出格式

所有命令支持 `-f` 参数：
- `table` - 表格（默认）
- `json` - JSON
- `yaml` - YAML
- `md` - Markdown
- `csv` - CSV

```bash
opencli <command> -f json      # JSON输出
opencli <command> -f yaml     # YAML输出
opencli <command> -v          # 详细模式（调试）
```

---

## 🇨🇳 中国平台专用指南

### ⚠️ 重要：中国平台反爬说明

中国平台（小红书、B站、知乎、微博）有较强的反爬机制，建议：

1. **优先使用Chrome DevTools MCP** 而非OpenCLI直接命令
2. **使用搜索结果页URL格式** 避免explore页面token验证问题
3. **注意登录状态** 某些数据需要登录才能访问

### 小红书 (xiaohongshu)

#### OpenCLI命令
```bash
opencli xiaohongshu search <关键词>        # 搜索
opencli xiaohongshu feed                   # 推荐 feed
opencli xiaohongshu user <user_id>         # 用户信息
opencli xiaohongshu download <note_id>     # 下载图片/视频
opencli xiaohongshu notifications         # 通知
```

#### Chrome DevTools 备用方案

当OpenCLI不可用时，使用Chrome DevTools MCP：

```bash
# 搜索结果页（推荐）
chrome-devtools navigate_page url="https://www.xiaohongshu.com/search_result?keyword=关键词&source=web_search_result_notes"

# 获取页面快照
chrome-devtools take_snapshot

# 点击帖子（使用take_snapshot返回的uid）
chrome-devtools click uid="xxx"
```

#### URL格式说明

| URL类型 | 格式 | 适用场景 |
|---------|------|---------|
| 搜索结果页 | `/search_result/xxx` | ✅ 推荐，可直接访问 |
| 帖子详情页 | `/explore/xxx` | ⚠️ 需要xsec_token验证 |
| 用户主页 | `/user/profile/xxx` | ✅ 可直接访问 |

#### 常见问题

| 问题 | 解决方案 |
|------|---------|
| 帖子返回404 | 使用搜索结果页URL而非explore页 |
| 空数据 | 确保已登录或检查页面加载 |
| 速度慢 | 使用chrome-devtools直接操作更稳定 |

### B站 (bilibili)

#### OpenCLI命令
```bash
opencli bilibili hot --limit 10              # 热门视频
opencli bilibili search <关键词>              # 搜索视频
opencli bilibili comments <bvid> --limit 20   # 评论区
opencli bilibili user-videos <uid>            # 用户视频
opencli bilibili dynamic                     # 用户动态
opencli bilibili feed                       # 关注动态
opencli bilibili history                    # 观看历史
opencli bilibili ranking                    # 排行榜
opencli bilibili download <bvid>             # 下载视频（需yt-dlp）
```

#### Chrome DevTools 备用方案

```bash
# 搜索
chrome-devtools navigate_page url="https://search.bilibili.com/all?keyword=关键词"

# 热门榜
chrome-devtools navigate_page url="https://www.bilibili.com/v/popular/rank/all"
```

### 知乎 (zhihu)

#### OpenCLI命令
```bash
opencli zhihu hot                           # 热榜
opencli zhihu search <关键词>               # 搜索
opencli zhihu download <url>                # 下载文章为Markdown
```

#### Chrome DevTools 备用方案

```bash
# 热榜
chrome-devtools navigate_page url="https://www.zhihu.com/hot"

# 搜索
chrome-devtools navigate_page url="https://www.zhihu.com/search?type=content&q=关键词"
```

#### 注意事项
- 知乎有时需要登录才能查看完整内容
- 验证码处理建议使用手动模式

### 微博 (weibo)

#### OpenCLI命令
```bash
opencli weibo hot                           # 热搜
opencli weibo search <关键词>              # 搜索
```

#### Chrome DevTools 备用方案

```bash
# 热搜榜
chrome-devtools navigate_page url="https://s.weibo.com/top/summary"

# 搜索
chrome-devtools navigate_page url="https://s.weibo.com/weibo?q=关键词"
```

---

## 国际平台

### Twitter/X
```bash
opencli twitter trending                    # 趋势
opencli twitter search <关键词>            # 搜索
opencli twitter timeline                   # 时间线
opencli twitter profile <user>             # 用户资料
opencli twitter bookmarks                  # 书签
opencli twitter post <text>              # 发推
opencli twitter download <user>          # 下载媒体
```

### Reddit
```bash
opencli reddit hot                         # 热门
opencli reddit frontpage                  # 首页
opencli reddit popular                    # 精华
opencli reddit search <关键词>            # 搜索
opencli reddit subreddit <name>           # 子版块
opencli reddit user <username>           # 用户
```

### Hacker News
```bash
opencli hackernews top                     # Top故事
opencli hackernews new                    # 最新
opencli hackernews best                   # 最佳
opencli hackernews ask                   # Ask HN
opencli hackernews show                  # Show HN
opencli hackernews jobs                  # 招聘
opencli hackernews user <username>       # 用户
```

### YouTube
```bash
opencli youtube search <关键词>            # 搜索
opencli youtube video <video_id>          # 视频信息
opencli youtube transcript <video_id>     # 字幕
```

### Spotify
```bash
opencli spotify status                    # 当前播放
opencli spotify play                     # 播放
opencli spotify pause                    # 暂停
opencli spotify next                      # 下一首
opencli spotify prev                      # 上一首
opencli spotify search <关键词>           # 搜索
opencli spotify queue                    # 播放队列
```

---

## 桌面应用

需要CDP连接：
```bash
opencli cursor status                     # Cursor IDE状态
opencli cursor send "<prompt>"           # 发送prompt
opencli cursor screenshot                # 截图

opencli chatgpt status                  # ChatGPT状态
opencli chatgpt send "<prompt>"        # 发送prompt

opencli notion search <关键词>           # 搜索页面
opencli notion read <page_id>           # 读取页面
opencli notion write <page_id> "<text>" # 写入页面
```

---

## 退出码

| 码 | 含义 | 解决方案 |
|----|------|---------|
| 0 | 成功 | - |
| 1 | 通用错误 | 查看错误信息 |
| 2 | 用法错误 | 检查命令语法 |
| 66 | 空结果 | 可能需要登录或等待加载 |
| 69 | 扩展未连接 | 运行`python scripts/diagnostic.py`诊断 |
| 75 | 超时 | 重试或使用chrome-devtools |
| 77 | 需要登录 | 登录目标网站 |
| 78 | 配置错误 | 检查chrome扩展状态 |

---

## AI Agent工作流

```bash
# 探索网站API
opencli explore <url> --site <name>

# 生成适配器
opencli synthesize <site>

# 一键生成命令
opencli generate <url> --goal "<目标>"

# 自动探测认证策略
opencli cascade <url>
```

---

## 常见问题

### 扩展未连接
```bash
# 详细诊断
python scripts/diagnostic.py

# 快速检查
opencli doctor
```

### 返回空数据
```bash
# 查看平台特定的备用方案
python scripts/fallback_manager.py xiaohongshu
python scripts/fallback_manager.py bilibili
python scripts/fallback_manager.py zhihu
```

### 高反爬网站
```bash
# 小红书等高反爬平台建议使用chrome-devtools
chrome-devtools navigate_page url="https://www.xiaohongshu.com/search_result?keyword=关键词"
chrome-devtools take_snapshot
```

### Windows路径问题
```bash
# 确保使用正确的BV号格式（BV开头）
# 例如: BV1xx411c7mD
```

---

## 反爬强度对照表

| 平台 | 反爬等级 | 推荐工具 | 备注 |
|------|---------|---------|------|
| 小红书 | 🔴 高 | Chrome DevTools | 搜索结果页URL更稳定 |
| B站 | 🔴 高 | Chrome DevTools | 需处理登录验证 |
| 知乎 | 🔴 高 | Chrome DevTools | 可能需要验证码 |
| 微博 | 🔴 高 | Chrome DevTools | 热搜需登录 |
| Twitter | 🟡 中 | Playwright | 较稳定 |
| Reddit | 🔵 低 | Agent-browser | 最易抓取 |
| HN | 🔵 低 | Agent-browser | 最易抓取 |
| YouTube | 🟡 中 | Playwright | 较稳定 |

---

## 工具选择决策树

```
开始
  │
  ├─ 扩展已连接？
  │   └─ 是 → 使用OpenCLI命令
  │   └─ 否 → 继续
  │
  ├─ 平台反爬等级？
  │   ├─ 低（HN, Reddit）→ Agent-browser
  │   ├─ 中（Twitter, YouTube）→ Playwright
  │   └─ 高（中国平台）→ Chrome DevTools
  │
  └─ 使用对应工具的操作命令
```