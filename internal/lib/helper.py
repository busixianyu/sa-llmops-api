from typing import Any
import importlib


def dynamic_import(module_name: str, symbol: str) -> Any:
    """动态导入模块"""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, symbol)
    except ImportError:
        raise ImportError(f"Failed to import {symbol} from {module_name}")
