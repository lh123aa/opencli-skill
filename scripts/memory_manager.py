#!/usr/bin/env python3
"""
OpenCLI Memory System
记忆系统 - 管理会话记忆、用户偏好、知识库
"""

import json
import yaml
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 数据目录
DATA_DIR = Path("C:/Users/49046/.config/opencode/skills/opencli/data")
MEMORY_DIR = DATA_DIR / "memory"
MEMORY_DIR.mkdir(parents=True, exist_ok=True)

# 文件路径
SESSION_FILE = MEMORY_DIR / "session-memory.json"
PREFERENCES_FILE = MEMORY_DIR / "user-preferences.yaml"
KNOWLEDGE_FILE = MEMORY_DIR / "knowledge-base.md"

# 默认偏好
DEFAULT_PREFERENCES = {
    "default_format": "table",
    "常用平台": [],
    "常用命令": [],
    "默认限制": 10,
    "输出目录": str(DATA_DIR / "outputs"),
    "auto_iteration_report": True,
}


class MemoryManager:
    """记忆管理器"""

    def __init__(self):
        self._init_files()

    def _init_files(self):
        """初始化记忆文件"""
        # 会话记忆
        if not SESSION_FILE.exists():
            self._save_session(
                {"operations": [], "session_start": datetime.now().isoformat()}
            )

        # 用户偏好
        if not PREFERENCES_FILE.exists():
            self._save_preferences(DEFAULT_PREFERENCES.copy())

        # 知识库
        if not KNOWLEDGE_FILE.exists():
            self._init_knowledge_base()

    def _load_session(self) -> Dict:
        """加载会话记忆"""
        try:
            with open(SESSION_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return {"operations": [], "session_start": datetime.now().isoformat()}

    def _save_session(self, data: Dict):
        """保存会话记忆"""
        with open(SESSION_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_preferences(self) -> Dict:
        """加载用户偏好"""
        try:
            with open(PREFERENCES_FILE, "r", encoding="utf-8") as f:
                return yaml.safe_load(f) or DEFAULT_PREFERENCES.copy()
        except:
            return DEFAULT_PREFERENCES.copy()

    def _save_preferences(self, data: Dict):
        """保存用户偏好"""
        with open(PREFERENCES_FILE, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    def _init_knowledge_base(self):
        """初始化知识库"""
        content = f"""# OpenCLI 知识库

> 创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 数据抓取记录

暂无记录。

---

## 平台统计

| 平台 | 抓取次数 | 最后抓取时间 |
|------|----------|--------------|
| - | - | - |

---

## 常用查询

暂无记录。

"""
        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            f.write(content)

    # ========== 会话记忆 ==========

    def add_operation(
        self,
        command: str,
        platform: str,
        result_summary: str,
        items_count: int = 0,
        status: str = "success",
    ) -> None:
        """添加操作到会话记忆"""
        session = self._load_session()
        operation = {
            "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "命令": command,
            "平台": platform,
            "结果摘要": result_summary,
            "条目数": items_count,
            "状态": status,
        }
        session["operations"].append(operation)
        # 只保留最近50条
        if len(session["operations"]) > 50:
            session["operations"] = session["operations"][-50:]
        self._save_session(session)

        # 更新偏好中的常用命令
        self._update_common_commands(command, platform)

    def get_session_history(self, limit: int = 10) -> List[Dict]:
        """获取会话历史"""
        session = self._load_session()
        return session["operations"][-limit:]

    def clear_session(self) -> None:
        """清空会话记忆"""
        self._save_session(
            {
                "operations": [],
                "session_start": datetime.now().isoformat(),
                "last_cleared": datetime.now().isoformat(),
            }
        )

    # ========== 用户偏好 ==========

    def get_preferences(self) -> Dict:
        """获取用户偏好"""
        return self._load_preferences()

    def update_preference(self, key: str, value: Any) -> None:
        """更新单个偏好"""
        prefs = self._load_preferences()
        prefs[key] = value
        self._save_preferences(prefs)

    def add_common_platform(self, platform: str) -> None:
        """添加常用平台"""
        prefs = self._load_preferences()
        platforms = prefs.get("常用平台", [])
        if platform not in platforms:
            platforms.append(platform)
            prefs["常用平台"] = platforms
            self._save_preferences(prefs)

    def _update_common_commands(self, command: str, platform: str) -> None:
        """更新常用命令统计"""
        prefs = self._load_preferences()
        commands = prefs.get("常用命令", [])
        # 简单去重保留最近20条
        cmd_entry = {
            "命令": command,
            "平台": platform,
            "时间": datetime.now().isoformat(),
        }
        commands = [c for c in commands if c.get("命令") != command]
        commands.append(cmd_entry)
        prefs["常用命令"] = commands[-20:]
        self._save_preferences(prefs)

    # ========== 知识库 ==========

    def add_knowledge(
        self,
        platform: str,
        data_type: str,
        query: str,
        count: int,
        summary: str,
        details: str = "",
    ) -> None:
        """添加知识到知识库"""
        # 读取现有知识库
        with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        # 更新抓取记录
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_record = f"""
### {platform} - {data_type}
- **查询**: {query}
- **时间**: {timestamp}
- **条目数**: {count}
- **摘要**: {summary}
{details}
"""

        # 在"数据抓取记录"部分后添加
        if "暂无记录" in content:
            content = content.replace("暂无记录。", f"暂无记录。{new_record}")
        else:
            # 找到最后一个 ### 位置插入
            parts = content.split("---")
            if len(parts) >= 2:
                parts[1] = parts[1].rstrip() + f"\n{new_record}\n"
                content = "---".join(parts)

        # 更新平台统计
        content = self._update_platform_stats(content, platform)

        with open(KNOWLEDGE_FILE, "w", encoding="utf-8") as f:
            f.write(content)

    def _update_platform_stats(self, content: str, platform: str) -> str:
        """更新平台统计"""
        timestamp = datetime.now().strftime("%Y-%m-%d")

        if platform in content:
            # 增加计数
            import re

            pattern = rf"(\| {re.escape(platform)} \|)(\d+)(\|)"
            match = re.search(pattern, content)
            if match:
                new_count = int(match.group(2)) + 1
                content = re.sub(pattern, rf"\1{new_count}\3", content)
            # 更新时间
            content = re.sub(
                rf"(\| {re.escape(platform)} \|\d+\|)([^\|]+)(\|)",
                rf"\1\2|{timestamp}|",
                content,
            )
        else:
            # 添加新平台
            stats_line = f"| {platform} | 1 | {timestamp} |\n"
            content = re.sub(r"(\| - \| - \| - \|)", stats_line, content)
        return content

    def query_knowledge(self, keyword: str) -> List[str]:
        """查询知识库"""
        results = []
        try:
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                content = f.read()

            import re

            # 简单关键词匹配
            sections = re.split(r"### ", content)
            for section in sections:
                if keyword.lower() in section.lower():
                    results.append(section.strip())
        except:
            pass
        return results

    def get_knowledge_stats(self) -> Dict:
        """获取知识库统计"""
        try:
            with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as f:
                content = f.read()

            import re

            stats = {}
            for match in re.finditer(r"\|\s*(\w+)\s*\|\s*(\d+)\s*\|", content):
                platform, count = match.groups()
                if platform != "-":
                    stats[platform] = int(count)
            return stats
        except:
            return {}

    # ========== 记忆系统状态 ==========

    def get_memory_status(self) -> Dict:
        """获取记忆系统状态"""
        session = self._load_session()
        prefs = self._load_preferences()
        stats = self.get_knowledge_stats()

        return {
            "session_operations": len(session.get("operations", [])),
            "session_start": session.get("session_start", "unknown"),
            "common_platforms": prefs.get("常用平台", []),
            "common_commands_count": len(prefs.get("常用命令", [])),
            "knowledge_platforms": list(stats.keys()),
            "total_knowledge_entries": sum(stats.values()),
        }


# CLI接口
if __name__ == "__main__":
    import sys

    manager = MemoryManager()

    if len(sys.argv) < 2:
        print("Usage: python memory_manager.py <action> [args]")
        print("Actions:")
        print("  status                      - 查看记忆状态")
        print("  add-op <cmd> <platform> <summary> [count] - 添加操作")
        print("  history [limit]             - 查看会话历史")
        print("  add-knowledge <platform> <type> <query> <count> <summary>")
        print("  query <keyword>            - 查询知识库")
        print("  get-prefs                  - 获取用户偏好")
        print("  set-pref <key> <value>     - 设置偏好")
        print("  clear-session              - 清空会话记忆")
        sys.exit(1)

    action = sys.argv[1]

    if action == "status":
        status = manager.get_memory_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))

    elif action == "add-op" and len(sys.argv) >= 5:
        cmd, platform, summary = sys.argv[2], sys.argv[3], sys.argv[4]
        count = int(sys.argv[5]) if len(sys.argv) > 5 else 0
        manager.add_operation(cmd, platform, summary, count)
        print("OK")

    elif action == "history":
        limit = int(sys.argv[2]) if len(sys.argv) > 2 else 10
        history = manager.get_session_history(limit)
        print(json.dumps(history, ensure_ascii=False, indent=2))

    elif action == "add-knowledge" and len(sys.argv) >= 7:
        platform, data_type, query = sys.argv[2], sys.argv[3], sys.argv[4]
        count = int(sys.argv[5])
        summary = sys.argv[6]
        manager.add_knowledge(platform, data_type, query, count, summary)
        print("OK")

    elif action == "query" and len(sys.argv) > 2:
        keyword = sys.argv[2]
        results = manager.query_knowledge(keyword)
        for r in results:
            print(r)

    elif action == "get-prefs":
        print(json.dumps(manager.get_preferences(), ensure_ascii=False, indent=2))

    elif action == "set-pref" and len(sys.argv) > 3:
        key, value = sys.argv[2], sys.argv[3]
        manager.update_preference(key, value)
        print("OK")

    elif action == "clear-session":
        manager.clear_session()
        print("Session cleared")
