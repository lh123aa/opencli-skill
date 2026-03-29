#!/usr/bin/env python3
"""
OpenCLI Iteration Engine
迭代引擎 - 问题追踪、改进建议、工作流学习、报告生成
"""

import json
import yaml
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional
from dataclasses import dataclass, asdict

# 数据目录
DATA_DIR = Path("C:/Users/49046/.config/opencode/skills/opencli/data")
ITERATION_DIR = DATA_DIR / "iteration"
REPORTS_DIR = ITERATION_DIR / "reports"
ITERATION_DIR.mkdir(parents=True, exist_ok=True)
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# 文件路径
PROBLEMS_FILE = ITERATION_DIR / "problems.json"
IMPROVEMENTS_FILE = ITERATION_DIR / "improvements.md"
WORKFLOWS_FILE = ITERATION_DIR / "workflows.yaml"

# 问题优先级
PRIORITY_CRITICAL = "critical"
PRIORITY_HIGH = "high"
PRIORITY_MEDIUM = "medium"
PRIORITY_LOW = "low"

# 问题状态
STATUS_OPEN = "open"
STATUS_IN_PROGRESS = "in_progress"
STATUS_RESOLVED = "resolved"
STATUS_WONT_FIX = "wont_fix"


@dataclass
class Problem:
    """问题记录"""

    id: str
    时间: str
    平台: str
    命令: str
    错误信息: str
    优先级: str
    状态: str
    标签: List[str]
    解决方案: str = ""
    迭代记录: List[Dict] = None

    def __post_init__(self):
        if self.迭代记录 is None:
            self.迭代记录 = []


class IterationEngine:
    """迭代引擎"""

    def __init__(self):
        self._init_files()
        self._problem_counter = self._load_problem_counter()

    def _init_files(self):
        """初始化文件"""
        # 问题记录
        if not PROBLEMS_FILE.exists():
            self._save_problems({"problems": [], "counter": 0})

        # 改进建议
        if not IMPROVEMENTS_FILE.exists():
            self._init_improvements()

        # 工作流
        if not WORKFLOWS_FILE.exists():
            self._save_workflows({"workflows": []})

    def _load_problems(self) -> Dict:
        with open(PROBLEMS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)

    def _save_problems(self, data: Dict):
        with open(PROBLEMS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def _load_problem_counter(self) -> int:
        try:
            data = self._load_problems()
            return data.get("counter", 0)
        except:
            return 0

    def _init_improvements(self):
        content = f"""# OpenCLI 改进建议

> 创建时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 待处理建议

暂无建议。

---

## 进行中

暂无。

---

## 已完成

暂无。

---

## 命令优化记录

| 时间 | 命令 | 优化内容 | 效果 |
|------|------|----------|------|
| - | - | - | - |

"""
        with open(IMPROVEMENTS_FILE, "w", encoding="utf-8") as f:
            f.write(content)

    def _load_workflows(self) -> Dict:
        with open(WORKFLOWS_FILE, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {"workflows": []}

    def _save_workflows(self, data: Dict):
        with open(WORKFLOWS_FILE, "w", encoding="utf-8") as f:
            yaml.dump(data, f, allow_unicode=True, default_flow_style=False)

    # ========== 问题管理 ==========

    def report_problem(
        self,
        platform: str,
        command: str,
        error: str,
        priority: str = PRIORITY_MEDIUM,
        tags: List[str] = None,
    ) -> str:
        """报告一个问题"""
        self._problem_counter += 1
        problem_id = f"P{self._problem_counter:04d}"

        problem = Problem(
            id=problem_id,
            时间=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            平台=platform,
            命令=command,
            错误信息=error,
            优先级=priority,
            状态=STATUS_OPEN,
            标签=tags or [],
        )

        data = self._load_problems()
        data["problems"].append(asdict(problem))
        data["counter"] = self._problem_counter
        self._save_problems(data)

        # 生成改进建议
        self._generate_improvement_suggestion(problem)

        return problem_id

    def update_problem_status(
        self, problem_id: str, status: str, solution: str = ""
    ) -> bool:
        """更新问题状态"""
        data = self._load_problems()
        for p in data["problems"]:
            if p["id"] == problem_id:
                p["状态"] = status
                if solution:
                    p["解决方案"] = solution
                p["迭代记录"].append(
                    {
                        "时间": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "操作": f"状态更新为 {status}",
                        "解决方案": solution,
                    }
                )
                self._save_problems(data)
                return True
        return False

    def get_problems(
        self, status: str = None, platform: str = None, priority: str = None
    ) -> List[Dict]:
        """获取问题列表"""
        data = self._load_problems()
        problems = data["problems"]

        if status:
            problems = [p for p in problems if p["状态"] == status]
        if platform:
            problems = [p for p in problems if p["平台"] == platform]
        if priority:
            problems = [p for p in problems if p["优先级"] == priority]

        return problems

    def get_problem_stats(self) -> Dict:
        """获取问题统计"""
        data = self._load_problems()
        problems = data["problems"]

        stats = {
            "total": len(problems),
            "open": len([p for p in problems if p["状态"] == STATUS_OPEN]),
            "in_progress": len(
                [p for p in problems if p["状态"] == STATUS_IN_PROGRESS]
            ),
            "resolved": len([p for p in problems if p["状态"] == STATUS_RESOLVED]),
            "by_platform": {},
            "by_priority": {
                PRIORITY_CRITICAL: 0,
                PRIORITY_HIGH: 0,
                PRIORITY_MEDIUM: 0,
                PRIORITY_LOW: 0,
            },
        }

        for p in problems:
            platform = p["平台"]
            stats["by_platform"][platform] = stats["by_platform"].get(platform, 0) + 1
            stats["by_priority"][p["优先级"]] += 1

        return stats

    def _generate_improvement_suggestion(self, problem: Problem):
        """为问题生成改进建议"""
        suggestions = []

        if "timeout" in problem.错误信息.lower():
            suggestions.append("- 增加命令超时时间")
            suggestions.append("- 添加重试机制")

        if "not connected" in problem.错误信息.lower():
            suggestions.append("- 检查Browser Bridge扩展连接")
            suggestions.append("- 考虑添加自动重连功能")

        if "login" in problem.错误信息.lower() or "auth" in problem.错误信息.lower():
            suggestions.append("- 优化登录状态检测")
            suggestions.append("- 添加登录引导提示")

        if "empty" in problem.错误信息.lower() or "[]" in problem.错误信息:
            suggestions.append("- 检查页面结构是否变化")
            suggestions.append("- 可能需要更新适配器选择器")

        if suggestions:
            self.add_improvement(
                category="问题修复",
                title=f"问题 #{problem.id} 的改进建议",
                description="\n".join(suggestions),
                related_problem=problem.id,
                priority=problem.优先级,
            )

    # ========== 改进建议 ==========

    def add_improvement(
        self,
        category: str,
        title: str,
        description: str,
        related_problem: str = "",
        priority: str = PRIORITY_MEDIUM,
        command: str = "",
        optimization: str = "",
    ) -> None:
        """添加改进建议"""
        with open(IMPROVEMENTS_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if optimization:
            # 命令优化记录
            new_entry = f"| {timestamp} | `{command}` | {optimization} | - |\n"
            content = re.sub(
                r"(\| - \| - \| - \| - \|)",
                f"| {timestamp} | `{command}` | {optimization} | - |\n| - | - | - | - |",
                content,
            )
        else:
            # 改进建议
            new_entry = f"""
### [{category}] {title}
- **时间**: {timestamp}
- **优先级**: {priority}
- **相关问题**: #{related_problem if related_problem else "无"}
- **描述**: {description}

"""
            if "暂无建议" in content:
                content = content.replace("暂无建议。", new_entry)
            else:
                content = content.replace(
                    "## 待处理建议\n\n暂无建议。", f"## 待处理建议\n\n{new_entry}"
                )

        with open(IMPROVEMENTS_FILE, "w", encoding="utf-8") as f:
            f.write(content)

    def add_command_optimization(
        self, command: str, before: str, after: str, effect: str
    ) -> None:
        """记录命令优化"""
        with open(IMPROVEMENTS_FILE, "r", encoding="utf-8") as f:
            content = f.read()

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = f"| {timestamp} | `{command}` | {before} → {after} | {effect} |\n"

        # 在表格最后一行前插入
        content = re.sub(
            r"(\| - \| - \| - \| - \|\n\n---)",
            f"{new_entry}| - | - | - | - |\n\n---",
            content,
        )

        with open(IMPROVEMENTS_FILE, "w", encoding="utf-8") as f:
            f.write(content)

    # ========== 工作流学习 ==========

    def learn_workflow(
        self, name: str, steps: List[Dict], platforms: List[str], tags: List[str] = None
    ) -> str:
        """学习一个新工作流"""
        workflow_id = f"W{len(self._load_workflows()['workflows']) + 1:03d}"

        workflow = {
            "id": workflow_id,
            "name": name,
            "platforms": platforms,
            "tags": tags or [],
            "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_used": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "use_count": 0,
            "steps": steps,
        }

        data = self._load_workflows()

        # 检查是否已存在相似工作流
        for i, w in enumerate(data["workflows"]):
            if w["name"] == name:
                # 更新现有工作流
                data["workflows"][i]["last_used"] = workflow["last_used"]
                data["workflows"][i]["use_count"] += 1
                self._save_workflows(data)
                return w["id"]

        data["workflows"].append(workflow)
        self._save_workflows(data)
        return workflow_id

    def get_workflows(self, platform: str = None, tag: str = None) -> List[Dict]:
        """获取工作流"""
        data = self._load_workflows()
        workflows = data["workflows"]

        if platform:
            workflows = [w for w in workflows if platform in w["platforms"]]
        if tag:
            workflows = [w for w in workflows if tag in w.get("tags", [])]

        return sorted(workflows, key=lambda x: x.get("use_count", 0), reverse=True)

    def use_workflow(self, workflow_id: str) -> Optional[Dict]:
        """使用工作流（增加计数）"""
        data = self._load_workflows()
        for w in data["workflows"]:
            if w["id"] == workflow_id:
                w["last_used"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                w["use_count"] = w.get("use_count", 0) + 1
                self._save_workflows(data)
                return w
        return None

    def get_workflow_stats(self) -> Dict:
        """获取工作流统计"""
        data = self._load_workflows()
        workflows = data["workflows"]

        return {
            "total": len(workflows),
            "total_uses": sum(w.get("use_count", 0) for w in workflows),
            "by_platform": self._count_by_field(workflows, "platforms"),
            "top_workflows": sorted(
                workflows, key=lambda x: x.get("use_count", 0), reverse=True
            )[:5],
        }

    def _count_by_field(self, items: List[Dict], field: str) -> Dict:
        counts = {}
        for item in items:
            for value in item.get(field, []):
                counts[value] = counts.get(value, 0) + 1
        return counts

    # ========== 报告生成 ==========

    def generate_report(self, session_summary: Dict = None) -> str:
        """生成迭代报告"""
        report_id = f"ITER-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        problem_stats = self.get_problem_stats()
        workflow_stats = self.get_workflow_stats()

        # 获取本次会话的问题
        session_problems = []
        if session_summary:
            for op in session_summary.get("operations", []):
                if op.get("status") != "success":
                    session_problems.append(op)

        report = f"""# OpenCLI 迭代报告

**报告ID**: {report_id}  
**生成时间**: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

---

## 执行摘要

| 指标 | 数值 |
|------|------|
| 会话操作数 | {session_summary.get("operation_count", "N/A") if session_summary else "N/A"} |
| 问题报告数 | {len(session_problems)} |
| 知识库新增 | {session_summary.get("knowledge_added", 0) if session_summary else 0} |

---

## 问题统计（全部时间）

| 状态 | 数量 |
|------|------|
| 待处理 | {problem_stats["open"]} |
| 进行中 | {problem_stats["in_progress"]} |
| 已解决 | {problem_stats["resolved"]} |
| **总计** | **{problem_stats["total"]}** |

### 按平台统计
"""

        for platform, count in problem_stats["by_platform"].items():
            report += f"| {platform} | {count} |\n"

        report += f"""
### 按优先级统计
| 优先级 | 数量 |
|--------|------|
| Critical | {problem_stats["by_priority"][PRIORITY_CRITICAL]} |
| High | {problem_stats["by_priority"][PRIORITY_HIGH]} |
| Medium | {problem_stats["by_priority"][PRIORITY_MEDIUM]} |
| Low | {problem_stats["by_priority"][PRIORITY_LOW]} |

---

## 改进建议摘要

"""

        # 读取改进建议
        try:
            with open(IMPROVEMENTS_FILE, "r", encoding="utf-8") as f:
                imp_content = f.read()

            # 提取待处理建议
            pending = re.findall(r"### \[.*?\] (.*?)\n", imp_content)
            if pending:
                report += f"**待处理建议**: {len(pending)} 项\n\n"
                for p in pending[:5]:
                    report += f"- {p}\n"
            else:
                report += "暂无待处理建议。\n"
        except:
            report += "无法读取改进建议。\n"

        report += f"""
---

## 工作流统计

| 指标 | 数值 |
|------|------|
| 已学习工作流 | {workflow_stats["total"]} |
| 总使用次数 | {workflow_stats["total_uses"]} |

### 常用工作流
"""

        for w in workflow_stats.get("top_workflows", []):
            report += f"- **{w['name']}** ({w.get('use_count', 0)}次使用)\n"

        report += f"""
---

## 本次会话问题

"""

        if session_problems:
            for p in session_problems:
                report += f"""### {p.get("platform", "Unknown")} - {p.get("command", "Unknown")}
- **错误**: {p.get("result_summary", p.get("错误信息", "Unknown error"))}
- **时间**: {p.get("时间", "Unknown")}

"""
        else:
            report += "本次会话无问题报告。\n"

        report += f"""
---

## 迭代建议

"""

        # 根据统计数据生成建议
        if problem_stats["open"] > 5:
            report += f"- ⚠️ 待处理问题较多（{problem_stats['open']}个），建议优先处理高优先级问题\n"

        if workflow_stats["total"] < 5:
            report += "- 💡 工作流学习不足，建议记录常用操作序列\n"

        if problem_stats["by_priority"][PRIORITY_CRITICAL] > 0:
            report += f"- 🔴 存在 {problem_stats['by_priority'][PRIORITY_CRITICAL]} 个严重问题，请立即处理\n"

        if not session_problems:
            report += "- ✅ 本次会话执行良好，无问题报告\n"

        report += f"""
---

## 下一步行动

"""

        open_problems = self.get_problems(
            status=STATUS_OPEN, priority=PRIORITY_CRITICAL
        )
        if open_problems:
            report += "### 紧急处理\n"
            for p in open_problems[:3]:
                report += f"- [ ] #{p['id']} {p['平台']}: {p['错误信息'][:50]}...\n"

        open_problems = self.get_problems(status=STATUS_OPEN, priority=PRIORITY_HIGH)
        if open_problems:
            report += "### 高优先级\n"
            for p in open_problems[:5]:
                report += f"- [ ] #{p['id']} {p['平台']}: {p['错误信息'][:50]}...\n"

        if not open_problems:
            report += "暂无待处理的紧急或高优先级问题。\n"

        report += f"""
---

*报告自动生成 by OpenCLI Iteration Engine*
"""

        # 保存报告
        report_file = REPORTS_DIR / f"{report_id}.md"
        with open(report_file, "w", encoding="utf-8") as f:
            f.write(report)

        return report_id, str(report_file)

    def get_iteration_status(self) -> Dict:
        """获取迭代系统状态"""
        return {
            "problem_stats": self.get_problem_stats(),
            "workflow_stats": self.get_workflow_stats(),
            "reports_count": len(list(REPORTS_DIR.glob("*.md"))),
            "last_report": None,
        }


# CLI接口
if __name__ == "__main__":
    import sys

    engine = IterationEngine()

    if len(sys.argv) < 2:
        print("Usage: python iteration_engine.py <action> [args]")
        print("Actions:")
        print("  status                        - 查看迭代状态")
        print("  report-problem <platform> <cmd> <error> [priority]")
        print("  update-status <id> <status> [solution]")
        print("  list-problems [status] [platform]")
        print("  problem-stats                 - 问题统计")
        print("  add-improvement <category> <title> <desc>")
        print("  add-optimization <cmd> <before> <after> <effect>")
        print("  learn-workflow <name> <steps_json>")
        print("  list-workflows [platform]")
        print("  workflow-stats                - 工作流统计")
        print("  generate-report [session_json]")
        sys.exit(1)

    action = sys.argv[1]

    if action == "status":
        print(json.dumps(engine.get_iteration_status(), ensure_ascii=False, indent=2))

    elif action == "report-problem" and len(sys.argv) >= 5:
        platform, cmd, error = sys.argv[2], sys.argv[3], sys.argv[4]
        priority = sys.argv[5] if len(sys.argv) > 5 else PRIORITY_MEDIUM
        pid = engine.report_problem(platform, cmd, error, priority)
        print(f"Reported: {pid}")

    elif action == "update-status" and len(sys.argv) >= 4:
        pid, status = sys.argv[2], sys.argv[3]
        solution = sys.argv[4] if len(sys.argv) > 4 else ""
        if engine.update_problem_status(pid, status, solution):
            print("Updated")
        else:
            print("Problem not found")

    elif action == "list-problems":
        status = sys.argv[2] if len(sys.argv) > 2 else None
        platform = sys.argv[3] if len(sys.argv) > 3 else None
        problems = engine.get_problems(status, platform)
        print(json.dumps(problems, ensure_ascii=False, indent=2))

    elif action == "problem-stats":
        print(json.dumps(engine.get_problem_stats(), ensure_ascii=False, indent=2))

    elif action == "add-improvement" and len(sys.argv) >= 5:
        cat, title, desc = sys.argv[2], sys.argv[3], sys.argv[4]
        engine.add_improvement(cat, title, desc)
        print("OK")

    elif action == "add-optimization" and len(sys.argv) >= 6:
        cmd, before, after, effect = sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
        engine.add_command_optimization(cmd, before, after, effect)
        print("OK")

    elif action == "learn-workflow" and len(sys.argv) >= 4:
        name = sys.argv[2]
        steps = json.loads(sys.argv[3])
        platforms = json.loads(sys.argv[4]) if len(sys.argv) > 4 else []
        wid = engine.learn_workflow(name, steps, platforms)
        print(f"Learned: {wid}")

    elif action == "list-workflows":
        platform = sys.argv[2] if len(sys.argv) > 2 else None
        workflows = engine.get_workflows(platform)
        print(json.dumps(workflows, ensure_ascii=False, indent=2))

    elif action == "workflow-stats":
        print(json.dumps(engine.get_workflow_stats(), ensure_ascii=False, indent=2))

    elif action == "generate-report":
        session_data = None
        if len(sys.argv) > 2:
            session_data = json.loads(sys.argv[2])
        report_id, report_path = engine.generate_report(session_data)
        print(f"Report generated: {report_id}")
        print(f"Path: {report_path}")
