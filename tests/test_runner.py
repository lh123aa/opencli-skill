#!/usr/bin/env python3
"""
test_runner.py - 测试运行器
"""

import os
import sys
import tempfile
from pathlib import Path

# 设置测试环境
os.environ["OPENCLI_DATA_DIR"] = tempfile.mkdtemp()

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))


def run_test_module(module_name: str) -> tuple:
    """运行测试模块"""
    try:
        module = __import__(module_name)
        # 运行main函数
        if hasattr(module, "main"):
            module.main()
            return True, None
        return True, None
    except Exception as e:
        return False, str(e)


def main():
    print("=" * 60)
    print("OpenCLI 测试套件")
    print("=" * 60)
    print()

    test_modules = [
        "test_config",
        "test_logger",
    ]

    passed = 0
    failed = 0
    results = []

    for module_name in test_modules:
        print(f"运行 {module_name}...")
        success, error = run_test_module(module_name)
        if success:
            passed += 1
            results.append((module_name, "✅", None))
        else:
            failed += 1
            results.append((module_name, "❌", error))
        print()

    print("=" * 60)
    print("测试汇总")
    print("=" * 60)

    for name, status, _ in results:
        print(f"  {status} {name}")

    print()
    print(f"结果: {passed} 通过, {failed} 失败")

    # Python语法检查
    print()
    print("=" * 60)
    print("Python语法检查")
    print("=" * 60)

    scripts_dir = Path(__file__).parent.parent / "scripts"
    syntax_ok = True

    for py_file in scripts_dir.rglob("*.py"):
        try:
            with open(py_file, "r", encoding="utf-8") as f:
                compile(f.read(), str(py_file), "exec")
            print(f"  ✅ {py_file.relative_to(scripts_dir)}")
        except SyntaxError as e:
            print(f"  ❌ {py_file.relative_to(scripts_dir)}: {e}")
            syntax_ok = False

    print()
    if syntax_ok:
        print("✅ 所有Python文件语法正确")
    else:
        print("❌ 存在语法错误")

    return 0 if failed == 0 and syntax_ok else 1


if __name__ == "__main__":
    sys.exit(main())
