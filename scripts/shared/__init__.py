"""
OpenCLI Shared Modules
跨平台共享模块
"""

from .config import (
    Config,
    config,
    get_data_dir,
    get_script_dir,
    ensure_dir,
    get_chrome_path,
    get_null_device,
    get_temp_dir,
    is_windows,
    is_macos,
    is_linux,
    Colors,
)

__all__ = [
    "Config",
    "config",
    "get_data_dir",
    "get_script_dir",
    "ensure_dir",
    "get_chrome_path",
    "get_null_device",
    "get_temp_dir",
    "is_windows",
    "is_macos",
    "is_linux",
    "Colors",
]
