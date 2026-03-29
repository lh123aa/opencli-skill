#!/usr/bin/env python3
"""
test_config.py - 配置模块测试
"""

import os
import sys
import tempfile
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

# 设置测试环境变量
os.environ["OPENCLI_DATA_DIR"] = tempfile.mkdtemp()

from shared.config import (
    Config,
    config,
    get_data_dir,
    get_chrome_path,
    get_null_device,
    is_windows,
    is_macos,
    is_linux,
    Colors,
)


class TestConfig:
    """配置模块测试"""

    def test_data_dir_from_env(self):
        """测试环境变量设置数据目录"""
        data_dir = get_data_dir()
        assert data_dir is not None
        assert isinstance(data_dir, Path)

    def test_null_device(self):
        """测试跨平台空设备路径"""
        null_dev = get_null_device()
        assert null_dev is not None
        if sys.platform == "win32":
            assert null_dev == "NUL"
        else:
            assert null_dev == "/dev/null"

    def test_platform_detection(self):
        """测试平台检测"""
        is_win = is_windows()
        is_mac = is_macos()
        is_lin = is_linux()

        # 至少一个平台为True
        assert is_win or is_mac or is_lin

        # 当前平台应该匹配sys.platform
        if sys.platform == "win32":
            assert is_win == True
        elif sys.platform == "darwin":
            assert is_mac == True
        else:
            assert is_lin == True

    def test_colors_class(self):
        """测试Colors类"""
        colors = Colors()
        assert hasattr(colors, "GREEN")
        assert hasattr(colors, "RED")
        assert hasattr(colors, "RESET")

    def test_config_singleton(self):
        """测试配置单例"""
        c1 = Config()
        c2 = Config()
        assert c1 is c2

    def test_chrome_path(self):
        """测试Chrome路径查找"""
        path = get_chrome_path()
        # 可能返回None（如果Chrome未安装）或返回字符串
        # 这个测试只是确保函数不抛出异常
        assert path is None or isinstance(path, str)


if __name__ == "__main__":
    test = TestConfig()
    print("运行配置模块测试...")

    tests = [
        ("环境变量数据目录", test.test_data_dir_from_env),
        ("空设备路径", test.test_null_device),
        ("平台检测", test.test_platform_detection),
        ("Colors类", test.test_colors_class),
        ("配置单例", test.test_config_singleton),
        ("Chrome路径", test.test_chrome_path),
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
