#!/usr/bin/env python3
"""
test_logger.py - 日志模块测试
"""

import os
import sys
import tempfile
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# 设置测试环境变量
os.environ["OPENCLI_DATA_DIR"] = tempfile.mkdtemp()

from shared.logger import get_logger, set_log_level, enable_file_logging


class TestLogger:
    """日志模块测试"""

    def test_get_logger(self):
        """测试获取日志实例"""
        logger = get_logger("test")
        assert logger is not None
        assert logger.name == "test"

    def test_same_logger_instance(self):
        """测试同一名称返回相同实例"""
        logger1 = get_logger("same_name")
        logger2 = get_logger("same_name")
        assert logger1 is logger2

    def test_different_loggers(self):
        """测试不同名称返回不同实例"""
        logger1 = get_logger("logger1")
        logger2 = get_logger("logger2")
        assert logger1 is not logger2

    def test_set_log_level(self):
        """测试设置日志级别"""
        set_log_level("DEBUG")
        set_log_level("INFO")
        set_log_level("WARNING")
        set_log_level("ERROR")
        # 不应抛出异常

    def test_enable_file_logging(self):
        """测试启用/禁用文件日志"""
        enable_file_logging(True)
        enable_file_logging(False)
        # 不应抛出异常

    def test_logger_methods(self):
        """测试日志方法存在"""
        logger = get_logger("methods_test")
        assert hasattr(logger, "debug")
        assert hasattr(logger, "info")
        assert hasattr(logger, "warning")
        assert hasattr(logger, "error")
        assert hasattr(logger, "critical")


if __name__ == "__main__":
    test = TestLogger()
    print("运行日志模块测试...")

    tests = [
        ("获取日志实例", test.test_get_logger),
        ("同一日志实例", test.test_same_logger_instance),
        ("不同日志实例", test.test_different_loggers),
        ("设置日志级别", test.test_set_log_level),
        ("启用文件日志", test.test_enable_file_logging),
        ("日志方法存在", test.test_logger_methods),
    ]

    passed = 0
    failed = 0

    for name, func in tests:
        try:
            func()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
