#!/usr/bin/env python3
"""
OpenCLI Shared Configuration
跨平台配置模块 - 统一管理所有配置路径和共享常量
"""

import os
import sys
import shutil
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

# 尝试导入yaml（可选）
try:
    import yaml

    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def get_data_dir() -> Path:
    """
    获取数据目录，支持环境变量自定义

    环境变量: OPENCLI_DATA_DIR
    默认: ~/.config/opencode/skills/opencli/data
    """
    env_dir = os.getenv("OPENCLI_DATA_DIR")
    if env_dir:
        return Path(env_dir).expanduser()

    # 跨平台默认路径
    if sys.platform == "win32":
        base = Path(os.getenv("APPDATA", Path.home() / "AppData" / "Roaming"))
        return base / "opencode" / "skills" / "opencli" / "data"
    else:
        return Path.home() / ".config" / "opencode" / "skills" / "opencli" / "data"


def get_script_dir() -> Path:
    """获取脚本所在目录"""
    return Path(__file__).parent.resolve()


def ensure_dir(path: Path) -> Path:
    """确保目录存在"""
    path.mkdir(parents=True, exist_ok=True)
    return path


def get_chrome_path() -> Optional[str]:
    """
    跨平台查找 Chrome 浏览器路径

    Returns:
        Chrome 路径字符串，或 None 如果未找到
    """
    # 1. 检查环境变量
    env_path = os.getenv("CHROME_PATH")
    if env_path and Path(env_path).exists():
        return env_path

    # 2. 使用 shutil.which 查找（跨平台）
    for cmd in ["chrome", "google-chrome", "chromium", "chromium-browser"]:
        path = shutil.which(cmd)
        if path:
            return path

    # 3. 常见平台特定路径
    if sys.platform == "win32":
        paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        ]
    elif sys.platform == "darwin":
        paths = [
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Chromium.app/Contents/MacOS/Chromium",
        ]
    else:
        paths = [
            "/usr/bin/google-chrome",
            "/usr/bin/chromium",
            "/usr/bin/chromium-browser",
            "/snap/bin/chromium",
        ]

    for path in paths:
        if Path(path).exists():
            return path

    return None


def get_null_device() -> str:
    """
    获取空设备路径（跨平台）

    Returns NUL on Windows, /dev/null on Unix-like systems.
    """
    if sys.platform == "win32":
        return "NUL"
    return "/dev/null"


def get_temp_dir() -> Path:
    """获取临时目录"""
    return Path(tempfile.gettempdir())


def is_windows() -> bool:
    """是否 Windows 平台"""
    return sys.platform == "win32"


def is_macos() -> bool:
    """是否 macOS 平台"""
    return sys.platform == "darwin"


def is_linux() -> bool:
    """是否 Linux 平台"""
    return sys.platform.startswith("linux")


# ========== 彩色输出 ==========


class Colors:
    """跨平台彩色输出支持"""

    # 检测是否支持颜色
    _supports_color = None

    @classmethod
    def supports_color(cls) -> bool:
        """检测终端是否支持颜色输出"""
        if cls._supports_color is not None:
            return bool(cls._supports_color)

        # Windows PowerShell/10+ 支持 ANSI
        if sys.platform == "win32":
            cls._supports_color = bool(os.getenv("TERM"))
        else:
            cls._supports_color = sys.stdout.isatty()

        return bool(cls._supports_color)

    @classmethod
    def enable_colors(cls):
        """强制启用颜色"""
        cls._supports_color = True

    @classmethod
    def disable_colors(cls):
        """强制禁用颜色"""
        cls._supports_color = False

    # 颜色代码（Windows 10+ 或 Unix 终端）
    # 检测是否应该启用颜色
    _use_ansi = sys.platform != "win32" or bool(os.getenv("TERM"))

    GREEN = "\033[92m" if _use_ansi else ""
    RED = "\033[91m" if _use_ansi else ""
    YELLOW = "\033[93m" if _use_ansi else ""
    BLUE = "\033[94m" if _use_ansi else ""
    RESET = "\033[0m" if _use_ansi else ""
    BOLD = "\033[1m" if _use_ansi else ""


# ========== 配置单例 ==========


class Config:
    """全局配置单例"""

    _instance = None
    _data_dir = None
    _yaml_config = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load_yaml_config()
        return cls._instance

    def _load_yaml_config(self):
        """从config.yaml加载配置"""
        self._yaml_config = {}

        if not HAS_YAML:
            return

        # 查找config.yaml
        possible_paths = [
            Path(__file__).parent.parent.parent / "config.yaml",  # 项目根目录
            get_data_dir() / "config.yaml",  # 数据目录
        ]

        for config_path in possible_paths:
            if config_path.exists():
                try:
                    with open(config_path, "r", encoding="utf-8") as f:
                        self._yaml_config = yaml.safe_load(f) or {}
                    break
                except Exception:
                    pass

    @property
    def yaml_config(self) -> Dict[str, Any]:
        """获取YAML配置"""
        return self._yaml_config

    def get(self, key: str, default: Any = None) -> Any:
        """
        获取配置值，支持点号分隔的路径如 'logging.level'

        Args:
            key: 配置键，支持嵌套如 'platforms.xiaohongshu.tool'
            default: 默认值

        Returns:
            配置值或默认值
        """
        keys = key.split(".")
        value = self._yaml_config

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
                if value is None:
                    return default
            else:
                return default

        return value if value is not None else default

    @property
    def data_dir(self) -> Path:
        """数据目录"""
        if self._data_dir is None:
            self._data_dir = get_data_dir()
            ensure_dir(self._data_dir)
        return self._data_dir

    @property
    def memory_dir(self) -> Path:
        """记忆系统目录"""
        return ensure_dir(self.data_dir / "memory")

    @property
    def iteration_dir(self) -> Path:
        """迭代系统目录"""
        return ensure_dir(self.data_dir / "iteration")

    @property
    def logs_dir(self) -> Path:
        """日志目录"""
        return ensure_dir(self.data_dir / "logs")

    @property
    def outputs_dir(self) -> Path:
        """输出目录"""
        return ensure_dir(self.data_dir / "outputs")

    @property
    def log_level(self) -> str:
        """获取日志级别"""
        return self.get("logging.level", "INFO")

    @property
    def log_file_enabled(self) -> bool:
        """是否启用文件日志"""
        return self.get("logging.file_enabled", True)

    @property
    def chrome_path(self) -> Optional[str]:
        """获取Chrome路径"""
        return self.get("chrome.path")

    @property
    def default_format(self) -> str:
        """获取默认输出格式"""
        return self.get("output.default_format", "table")

    def reset(self):
        """重置配置（用于测试）"""
        self._data_dir = None
        self._yaml_config = {}


# 全局配置实例
config = Config()
