#!/usr/bin/env python3
"""
OpenCLI - 命令行接口
通过浏览器自动化访问各类网站，获取结构化数据

用法:
    opencli doctor                    # 运行诊断
    opencli fallback <platform>       # 查看降级指南
    opencli memory <action>           # 记忆系统管理
    opencli iteration <action>       # 迭代引擎管理
    opencli --version                # 显示版本
    opencli --help                   # 显示帮助
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

# 添加shared模块路径
sys.path.insert(0, str(Path(__file__).parent / "shared"))
from config import config
from logger import get_logger

__version__ = "2.2.0"


def cmd_doctor(args):
    """运行诊断检查"""
    from diagnostic import DiagnosticSystem

    diagnostic = DiagnosticSystem()
    if args.json:
        import json

        report = diagnostic.run_all()
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        report = diagnostic.run_all()
        diagnostic.print_report(report)
    return 0 if report["summary"]["failed"] == 0 else 1


def cmd_fallback(args):
    """显示降级指南"""
    from fallback_manager import FallbackManager

    manager = FallbackManager()
    if args.action == "status":
        import json

        status = manager.check_extension_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    elif args.action == "stats":
        import json

        stats = manager.get_fallback_stats()
        print(json.dumps(stats, ensure_ascii=False, indent=2))
    else:
        manager.print_fallback_guide(args.platform or "xiaohongshu")
    return 0


def cmd_memory(args):
    """记忆系统管理"""
    from memory_manager import MemoryManager

    manager = MemoryManager()

    if args.subcmd == "status":
        import json

        status = manager.get_memory_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    elif args.subcmd == "history":
        import json

        history = manager.get_session_history(args.limit or 10)
        print(json.dumps(history, ensure_ascii=False, indent=2))
    elif args.subcmd == "clear":
        manager.clear_session()
        print("会话记忆已清空")
    elif args.subcmd == "query" and args.query:
        results = manager.query_knowledge(args.query)
        for r in results:
            print(r)
    elif args.subcmd == "prefs":
        import json

        prefs = manager.get_preferences()
        print(json.dumps(prefs, ensure_ascii=False, indent=2))
    else:
        print("用法: opencli memory <status|history|clear|query|prefs>")
    return 0


def cmd_iteration(args):
    """迭代引擎管理"""
    from iteration_engine import IterationEngine

    engine = IterationEngine()

    if args.subcmd == "status":
        import json

        status = engine.get_iteration_status()
        print(json.dumps(status, ensure_ascii=False, indent=2))
    elif args.subcmd == "problems":
        import json

        problems = engine.get_problems(args.status, args.platform)
        print(json.dumps(problems, ensure_ascii=False, indent=2))
    elif args.subcmd == "report":
        report_id, path = engine.generate_report()
        print(f"报告已生成: {report_id}")
        print(f"路径: {path}")
    elif args.subcmd == "stats":
        import json

        problem_stats = engine.get_problem_stats()
        workflow_stats = engine.get_workflow_stats()
        print("问题统计:")
        print(json.dumps(problem_stats, ensure_ascii=False, indent=2))
        print("\n工作流统计:")
        print(json.dumps(workflow_stats, ensure_ascii=False, indent=2))
    else:
        print("用法: opencli iteration <status|problems|report|stats>")
    return 0


def cmd_reporter(args):
    """任务报告生成"""
    from task_reporter import TaskReporter

    reporter = TaskReporter()

    if args.subcmd == "pending":
        reports = reporter.get_pending_reports()
        if reports:
            print("待处理报告:")
            for r in reports:
                print(f"  - {r['id']} ({r['modified']})")
        else:
            print("无待处理报告")
    elif args.subcmd == "complete" and args.report_id:
        if reporter.mark_as_completed(args.report_id):
            print(f"报告 {args.report_id} 已标记为完成")
        else:
            print(f"报告 {args.report_id} 不存在")
    elif args.subcmd == "generate":
        # 生成示例报告
        from task_reporter import (
            SEVERITY_HIGH,
            SEVERITY_MEDIUM,
            STATUS_PARTIAL,
        )

        report = reporter.create_report(
            task_name="示例任务",
            task_description="这是一个示例报告",
            status=STATUS_PARTIAL,
            completed_items=[
                {"description": "已完成项1", "status": True},
                {"description": "未完成项1", "status": False, "reason": "条件不满足"},
            ],
            data_stats=[
                {"type": "抓取", "count": 10, "unit": "个"},
            ],
            problems=[
                {
                    "description": "示例问题",
                    "severity": SEVERITY_HIGH,
                    "cause": "设计不足",
                },
            ],
            iterations=[
                {"timeline": "short", "description": "短期改进", "priority": "high"},
            ],
        )
        filepath = reporter.save_report(report, "pending")
        print(f"示例报告已生成: {filepath}")
        print()
        print(reporter.generate_markdown(report))
    else:
        print("用法: opencli reporter <pending|complete <id>|generate>")
    return 0


def main():
    parser = argparse.ArgumentParser(
        prog="opencli",
        description="OpenCLI - 浏览器自动化命令行工具",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  opencli doctor                    # 诊断检查
  opencli fallback xiaohongshu     # 小红书降级指南
  opencli memory status            # 记忆状态
  opencli iteration report         # 生成迭代报告

更多信息请访问: https://github.com/lh123aa/opencli-skill
""",
    )

    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    parser.add_argument("--debug", action="store_true", help="启用调试模式")

    subparsers = parser.add_subparsers(dest="command", help="可用命令")

    # doctor 命令
    doctor_parser = subparsers.add_parser("doctor", help="运行诊断检查")
    doctor_parser.add_argument("--json", action="store_true", help="JSON格式输出")

    # fallback 命令
    fallback_parser = subparsers.add_parser("fallback", help="查看降级指南")
    fallback_parser.add_argument(
        "platform", nargs="?", default="xiaohongshu", help="平台名称"
    )
    fallback_parser.add_argument(
        "action",
        nargs="?",
        default="guide",
        choices=["guide", "stats", "status"],
        help="操作",
    )

    # memory 命令
    memory_parser = subparsers.add_parser("memory", help="记忆系统管理")
    memory_parser.add_argument(
        "subcmd",
        nargs="?",
        default="status",
        choices=["status", "history", "clear", "query", "prefs"],
        help="子命令",
    )
    memory_parser.add_argument("--query", help="查询关键词")
    memory_parser.add_argument("--limit", type=int, help="限制数量")

    # iteration 命令
    iteration_parser = subparsers.add_parser("iteration", help="迭代引擎管理")
    iteration_parser.add_argument(
        "subcmd",
        nargs="?",
        default="status",
        choices=["status", "problems", "report", "stats"],
        help="子命令",
    )
    iteration_parser.add_argument("--status", help="问题状态过滤")
    iteration_parser.add_argument("--platform", help="平台过滤")

    # reporter 命令
    reporter_parser = subparsers.add_parser("reporter", help="任务报告生成")
    reporter_parser.add_argument(
        "subcmd",
        nargs="?",
        default="pending",
        choices=["pending", "complete", "generate"],
        help="子命令",
    )
    reporter_parser.add_argument("--report-id", help="报告ID")

    args = parser.parse_args()

    # 如果没有命令，显示帮助
    if not args.command:
        parser.print_help()
        return 0

    # 设置日志级别
    if args.debug:
        import logging
        from logger import set_log_level

        set_log_level("DEBUG")

    # 根据命令分发
    try:
        if args.command == "doctor":
            return cmd_doctor(args)
        elif args.command == "fallback":
            return cmd_fallback(args)
        elif args.command == "memory":
            return cmd_memory(args)
        elif args.command == "iteration":
            return cmd_iteration(args)
        elif args.command == "reporter":
            return cmd_reporter(args)
        else:
            parser.print_help()
            return 1
    except KeyboardInterrupt:
        print("\n已取消")
        return 130
    except Exception as e:
        print(f"错误: {e}")
        if args.debug:
            import traceback

            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
