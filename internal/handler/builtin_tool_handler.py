from injector import inject
from dataclasses import dataclass
from pkg.response import success_json
from internal.service import BuiltinToolService


@inject
@dataclass
class BuiltinToolHandler:
    """内置工具处理器"""
    builtin_tool_service: BuiltinToolService

    def get_builtin_tools(self):
        """获取内置工具信息+提供商信息"""
        builtin_tools = self.builtin_tool_service.get_builtin_tools()
        return success_json(data=builtin_tools)


    def get_provider_tool(self, provider_name:str, tool_name:str):
        """获取提供商信息"""
        pass

