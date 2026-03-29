#!/usr/bin/env python3
"""
OpenCLI Logging System
日志系统 - 统一管理所有脚本的日志输出
"""

import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

# 跨平台兼容导入
try:
    from .config import config, is_windows
except ImportError:
    # 当作为独立脚本运行时
    sys.path.insert(0, str(Path(__file__).parent.parent))
    from shared.config import config, is_windows


class ColoredFormatter(logging.Formatter):
    """彩色日志格式化器 - Windows兼容"""

    # 颜色代码
    COLORS = {
        "DEBUG": "\033[36m",  # 青色
        "INFO": "\033[32m",  # 绿色
        "WARNING": "\033[33m",  # 黄色
        "ERROR": "\033[31m",  # 红色
        "CRITICAL": "\033[35m",  # 紫色
    }
    RESET = "\033[0m"

    def __init__(self, fmt: str, use_color: bool = True):
        super().__init__(fmt)
        self.use_color = use_color and not is_windows()

    def format(self, record: logging.LogRecord) -> str:
        if self.use_color and record.levelname in self.COLORS:
            record.levelname = (
                f"{self.COLORS[record.levelname]}{record.levelname}{self.RESET}"
            )
        return super().format(record)


class OpenLogger:
    """OpenCLI日志管理器"""

    _instances = {}

    def __init__(self, name: str, log_file: Optional[Path] = None):
        self.name = name
        self.log_file = log_file or (config.logs_dir / f"{name}.log")
        self.logger = self._setup_logger()

    def _setup_logger(self) -> logging.Logger:
        """设置日志器"""
        logger = logging.getLogger(self.name)

        # 避免重复添加handler
        if logger.handlers:
            return logger

        logger.setLevel(logging.DEBUG)

        # 控制台处理器
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%H:%M:%S",
            use_color=True,
        )
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        # 文件处理器
        try:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            file_handler = logging.FileHandler(self.log_file, encoding="utf-8")
            file_handler.setLevel(logging.DEBUG)
            file_formatter = logging.Formatter(
                fmt="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
                datefmt="%Y-%m-%d %H:%M:%S",
            )
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)
        except Exception as e:
            logger.warning(f"无法创建日志文件: {e}")

        return logger

    @property
    def debug(self):
        return self.logger.debug

    @property
    def info(self):
        return self.logger.info

    @property
    def warning(self):
        return self.logger.warning

    @property
    def error(self):
        return self.logger.error

    @property
    def critical(self):
        return self.logger.critical

    def exception(self, msg: str):
        """记录异常并包含堆栈"""
        self.logger.exception(msg)


# 全局日志实例
_loggers = {}


def get_logger(name: str = "opencli") -> OpenLogger:
    """
    获取日志实例

    Args:
        name: 日志器名称，如 "diagnostic", "fallback", "memory"

    Returns:
        OpenLogger实例
    """
    if name not in _loggers:
        _loggers[name] = OpenLogger(name)
    return _loggers[name]


def set_log_level(level: str):
    """
    设置全局日志级别

    Args:
        level: DEBUG, INFO, WARNING, ERROR, CRITICAL
    """
    numeric_level = getattr(logging, level.upper(), logging.INFO)
    for logger in _loggers.values():
        logger.logger.setLevel(numeric_level)


def enable_file_logging(enabled: bool = True):
    """启用/禁用文件日志"""
    for logger in _loggers.values():
        for handler in logger.logger.handlers:
            if isinstance(handler, logging.FileHandler):
                handler.setLevel(logging.DEBUG if enabled else logging.CRITICAL)
