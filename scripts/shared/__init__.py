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
from .logger import (
    OpenLogger,
    get_logger,
    set_log_level,
    enable_file_logging,
)

__all__ = [
    # Config
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
    # Logger
    "OpenLogger",
    "get_logger",
    "set_log_level",
    "enable_file_logging",
]
