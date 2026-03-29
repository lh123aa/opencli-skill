# OpenCLI 命令参考

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
opencli <command> -v           # 详细模式（调试）
```

## 中国平台

### B站 (bilibili)
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

### 知乎 (zhihu)
```bash
opencli zhihu hot                           # 热榜
opencli zhihu search <关键词>               # 搜索
opencli zhihu download <url>                # 下载文章为Markdown
```

### 小红书 (xiaohongshu)
```bash
opencli xiaohongshu search <关键词>        # 搜索
opencli xiaohongshu feed                    # 推荐 feed
opencli xiaohongshu user <user_id>          # 用户信息
opencli xiaohongshu download <note_id>      # 下载图片/视频
opencli xiaohongshu notifications          # 通知
```

### 微博 (weibo)
```bash
opencli weibo hot                           # 热搜
opencli weibo search <关键词>              # 搜索
```

### 贴吧 (tieba)
```bash
opencli tieba hot                           # 热门帖子
opencli tieba posts <forum>                # 帖子列表
opencli tieba search <关键词>              # 搜索
```

## 国际平台

### Twitter/X
```bash
opencli twitter trending                    # 趋势
opencli twitter search <关键词>            # 搜索
opencli twitter timeline                   # 时间线
opencli twitter profile <user>             # 用户资料
opencli twitter bookmarks                  # 书签
opencli twitter post <text>               # 发推
opencli twitter download <user>           # 下载媒体
```

### Reddit
```bash
opencli reddit hot                         # 热门
opencli reddit frontpage                  # 首页
opencli reddit popular                    # 精华
opencli reddit search <关键词>            # 搜索
opencli reddit subreddit <name>            # 子版块
opencli reddit user <username>           # 用户
```

### Hacker News
```bash
opencli hackernews top                     # Top故事
opencli hackernews new                     # 最新
opencli hackernews best                   # 最佳
opencli hackernews ask                    # Ask HN
opencli hackernews show                   # Show HN
opencli hackernews jobs                   # 招聘
opencli hackernews user <username>        # 用户
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

## 桌面应用

需要CDP连接：
```bash
opencli cursor status                     # Cursor IDE状态
opencli cursor send "<prompt>"           # 发送prompt
opencli cursor screenshot                 # 截图

opencli chatgpt status                  # ChatGPT状态
opencli chatgpt send "<prompt>"        # 发送prompt

opencli notion search <关键词>           # 搜索页面
opencli notion read <page_id>           # 读取页面
opencli notion write <page_id> "<text>" # 写入页面
```

## 外部CLI枢纽

```bash
opencli gh pr list --limit 5            # GitHub CLI
opencli docker ps                        # Docker
opencli vercel deploy                   # Vercel
opencli obsidian search <关键词>         # Obsidian
```

## 注册自定义CLI

```bash
opencli register <name>                  # 注册本地CLI
opencli list                            # 查看包括自定义命令
```

## 插件

```bash
opencli plugin install <plugin>          # 安装插件
opencli plugin list                     # 列出插件
opencli plugin update <plugin>          # 更新插件
opencli plugin uninstall <plugin>       # 卸载插件
```

## 退出码

| 码 | 含义 |
|----|------|
| 0 | 成功 |
| 1 | 通用错误 |
| 2 | 用法错误 |
| 66 | 空结果 |
| 69 | 扩展未连接 |
| 75 | 超时 |
| 77 | 需要登录 |
| 78 | 配置错误 |

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

## 常见问题

**扩展未连接**
```bash
opencli doctor  # 检查状态
# 确保Chrome已打开且扩展已激活
```

**返回空数据**
- 检查Chrome是否已登录目标网站
- 尝试刷新登录状态

**Windows路径问题**
- 确保使用正确的BV号格式（BV开头）