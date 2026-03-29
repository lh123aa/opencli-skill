#!/usr/bin/env python3
"""
OpenCLI Fallback Manager
自动降级管理器 - 当扩展不可用时提供替代方案
"""

import json
import subprocess
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional


class FallbackTool(Enum):
    """备用工具枚举"""

    CHROME_DEVTOOLS = "chrome-devtools"
    PLAYWRIGHT = "playwright"
    AGENT_BROWSER = "agent-browser"
    MANUAL = "manual"


@dataclass
class FallbackRecommendation:
    """降级建议"""

    tool: FallbackTool
    confidence: float  # 0-1
    reason: str
    setup_instructions: str
    example_usage: str


class FallbackManager:
    """自动降级管理器"""

    # 平台反爬强度评估
    PLATFORM_ANTI_CRAWLING = {
        # 低反爬
        "hackernews": {"level": "low", "tool": FallbackTool.AGENT_BROWSER},
        "reddit": {"level": "low", "tool": FallbackTool.AGENT_BROWSER},
        # 中等反爬
        "twitter": {"level": "medium", "tool": FallbackTool.PLAYWRIGHT},
        "youtube": {"level": "medium", "tool": FallbackTool.PLAYWRIGHT},
        # 高反爬 - 中国平台
        "xiaohongshu": {"level": "high", "tool": FallbackTool.CHROME_DEVTOOLS},
        "bilibili": {"level": "high", "tool": FallbackTool.CHROME_DEVTOOLS},
        "zhihu": {"level": "high", "tool": FallbackTool.CHROME_DEVTOOLS},
        "weibo": {"level": "high", "tool": FallbackTool.CHROME_DEVTOOLS},
        # 极高反爬
        "wechat": {"level": "extreme", "tool": FallbackTool.MANUAL},
    }

    def __init__(self):
        self.data_dir = Path("C:/Users/49046/.config/opencode/skills/opencli/data")
        self.fallback_log = self.data_dir / "fallback_log.json"

    def check_extension_status(self) -> Dict:
        """检查扩展状态"""
        # 尝试执行一个简单的opencli命令来检测扩展
        try:
            result = subprocess.run(
                ["opencli", "doctor"], capture_output=True, text=True, timeout=10
            )

            if (
                "not connected" in result.stdout.lower()
                or "not connected" in result.stderr.lower()
            ):
                return {
                    "connected": False,
                    "error": "Extension not connected",
                    "suggestion": "Please activate the Chrome extension",
                }

            if result.returncode == 0:
                return {"connected": True, "output": result.stdout}
            else:
                return {
                    "connected": False,
                    "error": result.stderr,
                    "suggestion": "Try running 'opencli doctor' for details",
                }
        except FileNotFoundError:
            return {
                "connected": False,
                "error": "opencli command not found",
                "suggestion": "Please install opencli CLI",
            }
        except subprocess.TimeoutExpired:
            return {
                "connected": False,
                "error": "Command timeout",
                "suggestion": "Chrome extension may be unresponsive",
            }
        except Exception as e:
            return {
                "connected": False,
                "error": str(e),
                "suggestion": "Unknown error occurred",
            }

    def get_fallback_recommendation(self, platform: str) -> FallbackRecommendation:
        """获取平台对应的降级建议"""
        platform_lower = platform.lower()

        # 检查平台特定配置
        if platform_lower in self.PLATFORM_ANTI_CRAWLING:
            config = self.PLATFORM_ANTI_CRAWLING[platform_lower]
            return self._create_recommendation(
                tool=config["tool"],
                confidence=0.9,
                reason=f"{platform} has {config['level']} anti-crawling level",
                platform=platform_lower,
            )

        # 默认推荐
        return self._create_recommendation(
            tool=FallbackTool.CHROME_DEVTOOLS,
            confidence=0.5,
            reason="Default recommendation for unknown platforms",
            platform=platform_lower,
        )

    def _create_recommendation(
        self, tool: FallbackTool, confidence: float, reason: str, platform: str
    ) -> FallbackRecommendation:
        """创建降级建议"""

        instructions = {
            FallbackTool.CHROME_DEVTOOLS: """
**Chrome DevTools MCP** - 深度集成Chrome，调试能力强

1. 确保Chrome DevTools MCP已启用
2. 使用以下命令：

```bash
# 导航到页面
chrome-devtools navigate_page url="https://www.xiaohongshu.com"

# 获取快照
chrome-devtools take_snapshot

# 点击元素
chrome-devtools click uid="xxx"
```

推荐用于：高反爬网站、需要登录的页面、复杂交互
""",
            FallbackTool.PLAYWRIGHT: """
**Playwright MCP** - 跨浏览器支持，稳定性好

1. 确保Playwright MCP已启用
2. 使用以下命令：

```bash
# 导航
playwright_navigate url="https://example.com"

# 点击
playwright_click selector="button#submit"

# 提取文本
playwright_get_text selector="h1"
```

推荐用于：跨浏览器测试、数据抓取、表单操作
""",
            FallbackTool.AGENT_BROWSER: """
**Agent Browser** - Token效率最高，零配置

1. 确保Agent Browser已启用
2. 使用以下命令：

```bash
# 导航
navigate url="https://example.com"

# 创建快照
snapshot

# 使用引用操作
click ref="@e1"
```

推荐用于：简单自动化、代码验证、频繁迭代
""",
            FallbackTool.MANUAL: """
**手动操作** - 需要用户手动操作

某些平台（如微信）无法通过自动化工具访问，
建议：
1. 手动在浏览器中操作
2. 使用手机客户端
3. 考虑API服务（如有）
""",
        }

        example_usage = {
            FallbackTool.CHROME_DEVTOOLS: f"""
# 小红书搜索示例
chrome-devtools navigate_page url="https://www.xiaohongshu.com/search_result?keyword={platform}"
chrome-devtools take_snapshot
""",
            FallbackTool.PLAYWRIGHT: """
# 通用搜索示例
playwright_navigate url="https://www.google.com"
playwright_fill selector="input[name='q']" value="search query"
playwright_click selector="button[type='submit']"
""",
            FallbackTool.AGENT_BROWSER: """
# 简单导航示例
navigate url="https://example.com"
snapshot
click ref="@e1"  # 使用快照中的引用
""",
            FallbackTool.MANUAL: """
请手动在浏览器中完成操作。
""",
        }

        return FallbackRecommendation(
            tool=tool,
            confidence=confidence,
            reason=reason,
            setup_instructions=instructions.get(tool, "No instructions available"),
            example_usage=example_usage.get(tool, "No example available"),
        )

    def log_fallback_event(
        self, platform: str, original_error: str, fallback_tool: str
    ):
        """记录降级事件"""
        events = []
        if self.fallback_log.exists():
            try:
                with open(self.fallback_log, "r", encoding="utf-8") as f:
                    events = json.load(f)
            except:
                events = []

        events.append(
            {
                "timestamp": datetime.now().isoformat(),
                "platform": platform,
                "original_error": original_error,
                "fallback_tool": fallback_tool,
            }
        )

        # 只保留最近100条记录
        events = events[-100:]

        with open(self.fallback_log, "w", encoding="utf-8") as f:
            json.dump(events, f, ensure_ascii=False, indent=2)

    def get_fallback_stats(self) -> Dict:
        """获取降级统计"""
        if not self.fallback_log.exists():
            return {"total_fallbacks": 0, "by_tool": {}}

        try:
            with open(self.fallback_log, "r", encoding="utf-8") as f:
                events = json.load(f)

            stats = {"total_fallbacks": len(events), "by_tool": {}}
            for event in events:
                tool = event.get("fallback_tool", "unknown")
                stats["by_tool"][tool] = stats["by_tool"].get(tool, 0) + 1

            return stats
        except:
            return {"total_fallbacks": 0, "by_tool": {}}

    def print_fallback_guide(self, platform: str):
        """打印降级指南"""
        print(f"\n{'=' * 60}")
        print(f"🔄 OpenCLI 自动降级指南 - {platform}")
        print(f"{'=' * 60}\n")

        # 检查扩展状态
        status = self.check_extension_status()

        if status["connected"]:
            print("✅ Chrome扩展状态: 已连接")
            print("   opencli命令应该可以正常工作\n")
        else:
            print("❌ Chrome扩展状态: 未连接")
            print(f"   错误: {status.get('error', 'Unknown')}")
            print(f"   建议: {status.get('suggestion', 'N/A')}\n")

        # 获取推荐
        recommendation = self.get_fallback_recommendation(platform)

        print(f"📊 推荐工具: {recommendation.tool.value}")
        print(f"   置信度: {recommendation.confidence * 100:.0f}%")
        print(f"   原因: {recommendation.reason}\n")

        print(f"{'=' * 60}")
        print(f"📝 使用说明")
        print(f"{'=' * 60}")
        print(recommendation.setup_instructions)

        print(f"{'=' * 60}")
        print(f"💡 示例代码")
        print(f"{'=' * 60}")
        print(recommendation.example_usage)

        # 记录降级事件
        self.log_fallback_event(
            platform=platform,
            original_error=status.get("error", "extension not connected"),
            fallback_tool=recommendation.tool.value,
        )


# CLI接口
if __name__ == "__main__":
    import sys

    manager = FallbackManager()

    if len(sys.argv) < 2:
        print("Usage: python fallback_manager.py <platform> [action]")
        print("Actions:")
        print("  guide           - 显示降级指南 (默认)")
        print("  stats           - 显示降级统计")
        print("  status          - 检查扩展状态")
        sys.exit(1)

    platform = sys.argv[1]
    action = sys.argv[2] if len(sys.argv) > 2 else "guide"

    if action == "guide":
        manager.print_fallback_guide(platform)
    elif action == "stats":
        stats = manager.get_fallback_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    elif action == "status":
        status = manager.check_extension_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
