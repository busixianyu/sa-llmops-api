import io

from injector import inject
from dataclasses import dataclass
from pkg.response import success_json
from internal.service import BuiltinToolService
from flask import send_file


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
        builtin_tool = self.builtin_tool_service.get_provider_tool(provider_name, tool_name)
        return success_json(data=builtin_tool)

    def get_provider_icon(self, provider_name: str):
        """获取icon"""
        icon, icon_type = self.builtin_tool_service.get_provider_icon(provider_name)
        return send_file(io.BytesIO(icon), mimetype=icon_type)


    def get_provider_categories(self):
        """获取所有提供商的分类信息"""
        return success_json(data=self.builtin_tool_service.get_provider_categories())
