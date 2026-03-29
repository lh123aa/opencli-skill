#!/usr/bin/env python3
"""
OpenCLI Task Reporter
任务报告生成器 - 主动报告机制的核心组件
"""

import json
import re
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

# 跨平台兼容
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from config import config


# 严重程度枚举
SEVERITY_CRITICAL = "critical"
SEVERITY_HIGH = "high"
SEVERITY_MEDIUM = "medium"
SEVERITY_LOW = "low"

# 状态枚举
STATUS_SUCCESS = "success"
STATUS_PARTIAL = "partial"
STATUS_FAILED = "failed"


@dataclass
class CompletedItem:
    """已完成项"""

    description: str
    status: bool = True  # True=完成, False=未完成
    reason: str = ""


@dataclass
class DataStat:
    """数据统计"""

    type: str
    count: int
    unit: str = "条"


@dataclass
class Problem:
    """问题"""

    description: str
    severity: str  # critical, high, medium, low
    cause: str  # 工具限制, 设计不足, 用户误操作, 外部因素


@dataclass
class IterationItem:
    """迭代项"""

    timeline: str  # short, medium, long
    description: str
    priority: str


@dataclass
class TaskReport:
    """任务报告"""

    task_name: str
    task_description: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    status: str = STATUS_SUCCESS
    completed_items: List[CompletedItem] = field(default_factory=list)
    data_stats: List[DataStat] = field(default_factory=list)
    problems: List[Problem] = field(default_factory=list)
    iterations: List[IterationItem] = field(default_factory=list)
    files_created: List[str] = field(default_factory=list)
    notes: str = ""


class TaskReporter:
    """任务报告生成器"""

    def __init__(self):
        self._report_id = self._generate_report_id()
        self._init_dirs()

    def _init_dirs(self):
        """初始化目录"""
        self.reports_dir = config.iteration_dir / "reports"
        self.pending_dir = self.reports_dir / "pending"
        self.completed_dir = self.reports_dir / "completed"
        self.reports_dir.mkdir(parents=True, exist_ok=True)
        self.pending_dir.mkdir(parents=True, exist_ok=True)
        self.completed_dir.mkdir(parents=True, exist_ok=True)

    def _generate_report_id(self) -> str:
        """生成报告ID"""
        return f"TASK-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    def create_report(
        self,
        task_name: str,
        task_description: str,
        status: str = STATUS_SUCCESS,
        completed_items: List[Dict] = None,
        data_stats: List[Dict] = None,
        problems: List[Dict] = None,
        iterations: List[Dict] = None,
        files_created: List[str] = None,
        notes: str = "",
    ) -> TaskReport:
        """创建任务报告"""

        # 转换字典到dataclass
        completed = [
            CompletedItem(**item) if isinstance(item, dict) else item
            for item in (completed_items or [])
        ]

        stats = [
            DataStat(**stat) if isinstance(stat, dict) else stat
            for stat in (data_stats or [])
        ]

        problem_list = [
            Problem(**prob) if isinstance(prob, dict) else prob
            for prob in (problems or [])
        ]

        iteration_list = [
            IterationItem(**iter_item) if isinstance(iter_item, dict) else iter_item
            for iter_item in (iterations or [])
        ]

        return TaskReport(
            task_name=task_name,
            task_description=task_description,
            status=status,
            completed_items=completed,
            data_stats=stats,
            problems=problem_list,
            iterations=iteration_list,
            files_created=files_created or [],
            notes=notes,
        )

    def generate_markdown(self, report: TaskReport) -> str:
        """生成Markdown格式报告"""

        # 状态图标
        status_icons = {
            STATUS_SUCCESS: "✅",
            STATUS_PARTIAL: "⚠️",
            STATUS_FAILED: "❌",
        }
        status_icon = status_icons.get(report.status, "❓")

        # 严重程度图标
        severity_icons = {
            SEVERITY_CRITICAL: "🔴",
            SEVERITY_HIGH: "🟠",
            SEVERITY_MEDIUM: "🟡",
            SEVERITY_LOW: "🔵",
        }

        # 时间线图标
        timeline_labels = {
            "short": "短期（本次可修复）",
            "medium": "中期（需要改skill）",
            "long": "长期（架构优化）",
        }

        # 构建报告
        lines = [
            f"# 📋 任务完成报告",
            "",
            f"**报告ID**: {self._report_id}",
            f"**任务**: {report.task_name}",
            f"**时间**: {report.timestamp}",
            f"**状态**: {status_icon} {'完成' if report.status == STATUS_SUCCESS else '部分完成' if report.status == STATUS_PARTIAL else '失败'}",
            "",
            "---",
            "",
            "## ✅ 完成情况",
            "",
        ]

        # 完成情况
        if report.completed_items:
            for item in report.completed_items:
                icon = "✅" if item.status else "❌"
                line = f"- [{icon}] {item.description}"
                if item.reason and not item.status:
                    line += f"（原因：{item.reason}）"
                lines.append(line)
        else:
            lines.append("_无_")
            lines.append("")

        # 数据统计
        lines.extend(
            [
                "",
                "## 📊 数据统计",
                "",
            ]
        )

        if report.data_stats:
            lines.append("| 类型 | 数量 |")
            lines.append("|------|------|")
            for stat in report.data_stats:
                lines.append(f"| {stat.type} | {stat.count} {stat.unit} |")
        else:
            lines.append("_无统计数据_")
        lines.append("")

        # 遇到的问题
        lines.extend(
            [
                "",
                "## ⚠️ 遇到的问题",
                "",
            ]
        )

        if report.problems:
            lines.append("| 问题 | 严重程度 | 原因 |")
            lines.append("|------|---------|------|")
            for prob in report.problems:
                sev_icon = severity_icons.get(prob.severity, "❓")
                lines.append(
                    f"| {prob.description} | {sev_icon} {prob.severity} | {prob.cause} |"
                )
        else:
            lines.append("_无问题_")
        lines.append("")

        # 迭代方案
        lines.extend(
            [
                "",
                "## 🔧 迭代方案",
                "",
            ]
        )

        if report.iterations:
            for timeline in ["short", "medium", "long"]:
                items = [i for i in report.iterations if i.timeline == timeline]
                if items:
                    lines.append(f"**{timeline_labels.get(timeline, timeline)}**：")
                    for item in items:
                        lines.append(f"- {item.description}")
                    lines.append("")
        else:
            lines.append("_无迭代建议_")
            lines.append("")

        # 创建的文件
        if report.files_created:
            lines.extend(
                [
                    "",
                    "## 📁 创建的文件",
                    "",
                ]
            )
            for f in report.files_created:
                lines.append(f"- `{f}`")
            lines.append("")

        # 备注
        if report.notes:
            lines.extend(
                [
                    "",
                    "## 📝 备注",
                    "",
                    report.notes,
                    "",
                ]
            )

        # 询问
        lines.extend(
            [
                "",
                "---",
                "",
                "**需要我升级迭代吗？允许后立即执行。**",
            ]
        )

        return "\n".join(lines)

    def save_report(self, report: TaskReport, save_to: str = "pending") -> str:
        """保存报告"""
        content = self.generate_markdown(report)

        if save_to == "pending":
            filepath = self.pending_dir / f"{self._report_id}.md"
        elif save_to == "completed":
            filepath = self.completed_dir / f"{self._report_id}.md"
        else:
            filepath = self.reports_dir / f"{self._report_id}.md"

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

        return str(filepath)

    def get_pending_reports(self) -> List[Dict]:
        """获取待处理报告列表"""
        reports = []
        for f in self.pending_dir.glob("*.md"):
            stat = f.stat()
            reports.append(
                {
                    "id": f.stem,
                    "path": str(f),
                    "modified": datetime.fromtimestamp(stat.st_mtime).isoformat(),
                }
            )
        return sorted(reports, key=lambda x: x["modified"], reverse=True)

    def mark_as_completed(self, report_id: str) -> bool:
        """标记报告为已完成"""
        pending_file = self.pending_dir / f"{report_id}.md"
        if pending_file.exists():
            # 移动到completed目录
            completed_file = self.completed_dir / f"{report_id}.md"
            pending_file.rename(completed_file)
            return True
        return False


# CLI接口
if __name__ == "__main__":
    reporter = TaskReporter()

    if len(sys.argv) < 2:
        print("Usage: python task_reporter.py <action> [args]")
        print("Actions:")
        print("  create <task_name> <description>   - 创建报告")
        print("  pending                          - 查看待处理报告")
        print("  complete <report_id>            - 标记为已完成")
        print("  generate                         - 生成示例报告")
        sys.exit(1)

    action = sys.argv[1]

    if action == "create" and len(sys.argv) >= 4:
        task_name = sys.argv[2]
        description = sys.argv[3]

        # 解析可选参数
        status = STATUS_SUCCESS
        completed_items = []
        data_stats = []
        problems = []
        iterations = []

        # 简单解析：从JSON文件加载（如果有）
        # 实际使用时由Agent构建完整报告对象
        report = reporter.create_report(
            task_name=task_name,
            task_description=description,
            status=status,
            completed_items=completed_items,
            data_stats=data_stats,
            problems=problems,
            iterations=iterations,
        )

        filepath = reporter.save_report(report, "pending")
        print(f"Report created: {filepath}")
        print()
        print(reporter.generate_markdown(report))

    elif action == "pending":
        reports = reporter.get_pending_reports()
        if reports:
            print("待处理报告：")
            for r in reports:
                print(f"  - {r['id']} ({r['modified']})")
        else:
            print("无待处理报告")

    elif action == "complete" and len(sys.argv) >= 3:
        report_id = sys.argv[2]
        if reporter.mark_as_completed(report_id):
            print(f"报告 {report_id} 已标记为完成")
        else:
            print(f"报告 {report_id} 不存在")

    elif action == "generate":
        # 生成示例报告
        report = reporter.create_report(
            task_name="抓取小红书卡塔尔旅游帖子",
            task_description="抓取小红书上关于'卡塔尔旅游'的热帖前50个，并获取评论",
            status=STATUS_PARTIAL,
            completed_items=[
                {"description": "抓取小红书卡塔尔旅游热帖", "status": True},
                {"description": "获取帖子评论内容", "status": True, "reason": ""},
                {"description": "保存为markdown文件", "status": True},
                {
                    "description": "抓取50个帖子",
                    "status": False,
                    "reason": "用户要求只抓取10个",
                },
            ],
            data_stats=[
                {"type": "抓取帖子", "count": 10, "unit": "个"},
                {"type": "获取评论", "count": 156, "unit": "条"},
                {"type": "保存文件", "count": 1, "unit": "个"},
            ],
            problems=[
                {
                    "description": "opencli Chrome扩展连接失败",
                    "severity": SEVERITY_HIGH,
                    "cause": "工具限制",
                },
                {
                    "description": "帖子详情页URL返回404",
                    "severity": SEVERITY_MEDIUM,
                    "cause": "设计不足",
                },
            ],
            iterations=[
                {
                    "timeline": "short",
                    "description": "添加URL格式自动检测和备用格式尝试机制",
                    "priority": "high",
                },
                {
                    "timeline": "medium",
                    "description": "为小红书等高反爬平台添加Chrome DevTools备用方案",
                    "priority": "high",
                },
                {
                    "timeline": "long",
                    "description": "实现多工具自动协作流程",
                    "priority": "medium",
                },
            ],
            files_created=["E:\\程序\\小红书\\卡塔尔旅游热帖评论.md"],
            notes="用户临时修改需求为只抓取10个帖子",
        )

        filepath = reporter.save_report(report, "pending")
        print(f"示例报告已生成: {filepath}")
        print()
        print(reporter.generate_markdown(report))
