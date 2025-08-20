import datetime
from typing import Any

from langchain_core.tools import BaseTool


class CurrentTimeTool(BaseTool):
    """返回当前时间"""
    name:str = "current_time"
    description:str = "获取当前日期工具"

    def _run(self, *args: Any, **kwargs: Any) -> Any:
        """获取当前系统时间，格式化后返回"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S %Z")


def current_time(**kwargs) -> BaseTool:
    """返回当前时间"""
    return CurrentTimeTool()
