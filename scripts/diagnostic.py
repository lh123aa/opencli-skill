#!/usr/bin/env python3
"""
OpenCLI Diagnostic System
增强诊断系统 - 详细检查连接状态，提供修复建议
"""

import json
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# 跨平台兼容
sys.path.insert(0, str(Path(__file__).parent.parent / "shared"))
from config import (
    Colors,
    get_chrome_path,
    get_null_device,
    is_windows,
    is_linux,
    config,
)


@dataclass
class DiagnosticResult:
    """诊断结果"""

    name: str
    status: str  # "pass", "fail", "warn"
    message: str
    details: str = ""
    fix_suggestion: str = ""


class DiagnosticSystem:
    """增强诊断系统"""

    # Chrome扩展ID
    EXTENSION_ID = "opencli-browser-bridge"

    def __init__(self):
        self.results: List[DiagnosticResult] = []

    def run_all(self) -> Dict:
        """运行所有诊断"""
        self.results = []

        # 1. Chrome浏览器检查
        self._check_chrome()

        # 2. Chrome扩展检查
        self._check_extension()

        # 3. Node.js检查
        self._check_node()

        # 4. opencli CLI检查
        self._check_opencli()

        # 5. 网络连接检查
        self._check_network()

        # 6. 平台可用性检查
        self._check_platforms()

        return self._generate_report()

    def _check_chrome(self):
        """检查Chrome浏览器"""
        # 使用跨平台方法查找Chrome
        chrome_path = get_chrome_path()

        if chrome_path:
            self.results.append(
                DiagnosticResult(
                    name="Chrome浏览器",
                    status="pass",
                    message=f"✅ 已安装: {chrome_path}",
                    details=f"路径: {chrome_path}",
                )
            )
        else:
            self.results.append(
                DiagnosticResult(
                    name="Chrome浏览器",
                    status="fail",
                    message="❌ 未找到Chrome浏览器",
                    fix_suggestion="请安装 Google Chrome: https://www.google.com/chrome/",
                )
            )

    def _check_extension(self):
        """检查Browser Bridge扩展"""
        # 检查扩展是否在Chrome中启用
        # 注意：无法直接检查扩展启用状态，需要用户确认

        self.results.append(
            DiagnosticResult(
                name="Browser Bridge扩展",
                status="warn",
                message="⚠️ 请手动确认扩展已启用",
                details="在Chrome地址栏输入 chrome://extensions/ 检查",
                fix_suggestion="1. 打开 Chrome\n2. 访问 chrome://extensions/\n3. 确认 'OpenCLI Browser Bridge' 已启用\n4. 扩展图标应出现在工具栏",
            )
        )

        # 添加扩展连接检测说明
        self.results.append(
            DiagnosticResult(
                name="扩展连接状态",
                status="warn",
                message="⚠️ 需要手动测试连接",
                details="点击Chrome工具栏中的扩展图标，确认连接成功",
                fix_suggestion="如果扩展显示'未连接'：\n1. 点击扩展图标\n2. 等待连接建立\n3. 刷新目标页面",
            )
        )

    def _check_node(self):
        """检查Node.js"""
        try:
            result = subprocess.run(
                ["node", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=is_windows(),  # Windows需要shell=True
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.results.append(
                    DiagnosticResult(
                        name="Node.js",
                        status="pass",
                        message=f"✅ 已安装: v{version}",
                        details=f"版本: {version}",
                    )
                )
            else:
                raise Exception("Node.js not found")
        except Exception:
            self.results.append(
                DiagnosticResult(
                    name="Node.js",
                    status="fail",
                    message="❌ 未找到Node.js",
                    fix_suggestion="安装 Node.js: https://nodejs.org/",
                )
            )

    def _check_opencli(self):
        """检查opencli CLI"""
        try:
            result = subprocess.run(
                ["opencli", "--version"],
                capture_output=True,
                text=True,
                timeout=5,
                shell=is_windows(),
            )
            if result.returncode == 0:
                version = result.stdout.strip()
                self.results.append(
                    DiagnosticResult(
                        name="OpenCLI CLI",
                        status="pass",
                        message=f"✅ CLI已安装",
                        details=f"版本: {version}",
                    )
                )
            else:
                raise Exception("opencli not found")
        except Exception:
            self.results.append(
                DiagnosticResult(
                    name="OpenCLI CLI",
                    status="fail",
                    message="❌ 未找到opencli命令",
                    fix_suggestion="请安装 OpenCLI CLI:\nnpm install -g opencli",
                )
            )

    def _check_network(self):
        """检查网络连接"""
        test_urls = [
            ("Google", "https://www.google.com"),
            ("Chrome Web Store", "https://chrome.google.com"),
        ]

        for name, url in test_urls:
            try:
                # 使用Python的urllib代替curl命令（跨平台）
                import urllib.request
                import urllib.error

                req = urllib.request.Request(url, method="HEAD")
                urllib.request.urlopen(req, timeout=10)
                self.results.append(
                    DiagnosticResult(
                        name=f"网络-{name}",
                        status="pass",
                        message=f"✅ {name} 可访问",
                        details=f"HTTP 200",
                    )
                )
            except Exception:
                self.results.append(
                    DiagnosticResult(
                        name=f"网络-{name}",
                        status="warn",
                        message=f"⚠️ {name} 访问受限",
                        fix_suggestion="检查网络代理设置，或切换网络环境",
                    )
                )

    def _check_platforms(self):
        """检查目标平台可用性"""
        platforms = {
            "小红书": "https://www.xiaohongshu.com",
            "B站": "https://www.bilibili.com",
            "知乎": "https://www.zhihu.com",
        }

        for name, url in platforms.items():
            try:
                import urllib.request
                import urllib.error

                req = urllib.request.Request(url, method="HEAD")
                urllib.request.urlopen(req, timeout=10)
                self.results.append(
                    DiagnosticResult(
                        name=f"平台-{name}",
                        status="pass",
                        message=f"✅ {name} 可访问",
                        details=f"URL: {url}",
                    )
                )
            except Exception:
                self.results.append(
                    DiagnosticResult(
                        name=f"平台-{name}",
                        status="warn",
                        message=f"⚠️ {name} 访问异常",
                        fix_suggestion=f"可能需要登录或存在区域限制\nURL: {url}",
                    )
                )

    def _generate_report(self) -> Dict:
        """生成诊断报告"""
        passed = sum(1 for r in self.results if r.status == "pass")
        failed = sum(1 for r in self.results if r.status == "fail")
        warnings = sum(1 for r in self.results if r.status == "warn")

        report = {
            "timestamp": datetime.now().isoformat(),
            "summary": {
                "total": len(self.results),
                "passed": passed,
                "failed": failed,
                "warnings": warnings,
            },
            "results": [
                {
                    "name": r.name,
                    "status": r.status,
                    "message": r.message,
                    "details": r.details,
                    "fix_suggestion": r.fix_suggestion,
                }
                for r in self.results
            ],
            "overall_status": "healthy" if failed == 0 else "unhealthy",
            "next_steps": self._get_next_steps(failed, warnings),
        }

        return report

    def _get_next_steps(self, failed: int, warnings: int) -> List[str]:
        """获取下一步建议"""
        steps = []

        if failed > 0:
            steps.append("🔴 存在失败项，请先修复后再继续")
        elif warnings > 0:
            steps.append("🟡 存在警告项，请确认以下配置：")
            steps.append("   - 手动确认Chrome扩展已启用并连接")
        else:
            steps.append("🟢 所有检查通过！")

        steps.append("")
        steps.append("如果仍有问题，请尝试：")
        steps.append("   1. 重启Chrome浏览器")
        steps.append("   2. 重新安装Browser Bridge扩展")
        steps.append("   3. 使用备用方案: chrome-devtools MCP")

        return steps

    def print_report(self, report: Dict):
        """打印诊断报告"""
        print(f"\n{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{Colors.BOLD}🔍 OpenCLI 诊断报告{Colors.RESET}")
        print(f"{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"时间: {report['timestamp']}")
        print()

        # 摘要
        summary = report["summary"]
        print(
            f"📊 摘要: {summary['passed']} ✅ | {summary['warnings']} ⚠️ | {summary['failed']} ❌"
        )
        print()

        # 详细结果
        for r in report["results"]:
            status_icon = {
                "pass": f"{Colors.GREEN}✅",
                "fail": f"{Colors.RED}❌",
                "warn": f"{Colors.YELLOW}⚠️",
            }.get(r["status"], "❓")

            print(f"{status_icon} {Colors.BOLD}{r['name']}{Colors.RESET}")
            print(f"   {r['message']}")

            if r.get("details"):
                print(f"   {Colors.BLUE}详情: {r['details']}{Colors.RESET}")

            if r.get("fix_suggestion"):
                print(f"   {Colors.YELLOW}修复: {r['fix_suggestion']}{Colors.RESET}")
            print()

        # 下一步
        print(f"{Colors.BOLD}{'-' * 60}{Colors.RESET}")
        for step in report["next_steps"]:
            print(f"  {step}")
        print()

        # 总体状态
        if report["overall_status"] == "healthy":
            print(
                f"{Colors.GREEN}{Colors.BOLD}🎉 系统健康，可以正常使用！{Colors.RESET}"
            )
        else:
            print(
                f"{Colors.RED}{Colors.BOLD}⚠️ 系统存在问题，请修复后再使用{Colors.RESET}"
            )
        print()


# CLI接口
if __name__ == "__main__":
    diagnostic = DiagnosticSystem()

    if len(sys.argv) > 1 and sys.argv[1] == "--json":
        # JSON格式输出
        report = diagnostic.run_all()
        print(json.dumps(report, ensure_ascii=False, indent=2))
    else:
        # 人类可读格式输出
        report = diagnostic.run_all()
        diagnostic.print_report(report)

        # 退出码
        sys.exit(1 if report["summary"]["failed"] > 0 else 0)
