from typing import Any
import importlib


def dynamic_import(module_name: str, symbol: str) -> Any:
    """动态导入模块"""
    try:
        module = importlib.import_module(module_name)
        return getattr(module, symbol)
    except ImportError:
        raise ImportError(f"Failed to import {symbol} from {module_name}")


def add_attribute(attr_name: str, attr_value: Any):
    """装饰器函数"""
    def decorator(func):
        setattr(func, attr_name, attr_value)
        return func

    return decorator