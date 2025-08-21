import mimetypes
import os.path
from dataclasses import dataclass
from unicodedata import category

from injector import inject
from pydantic import BaseModel

from internal.core.tool.builtin_tool.provider import BuiltinProviderManager
from internal.exception import NotFoundException

from flask import current_app


@inject
@dataclass
class BuiltinToolService:
    """
    服务层：处理请求，调用对应服务，返回结果
    """

    builtin_provider_manager: BuiltinProviderManager

    def get_builtin_tools(self) -> list:
        providers = self.builtin_provider_manager.get_providers()
        builtin_tools = []
        for provider in providers:
            provider_entity = provider.provider_entity
            builtin_tool = {
                **provider_entity.model_dump(exclude={"icon", }),
                "tools": []
            }

            for tool_entity in provider.get_tool_entities():
                tool = provider.get_tool(tool_entity.name)
                tool_dict = {**tool_entity.model_dump(), "inputs": self.get_tool_inputs(tool)}
                builtin_tool["tools"].append(tool_dict)

            builtin_tools.append(builtin_tool)
        return builtin_tools

    def get_provider_tool(self, provider_name: str, tool_name: str) -> dict:
        # 获取指定提供者和工具的信息
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"该提供商{provider_name}不存在")

        tool_entity = provider.get_tool_entity(tool_name)
        if tool_entity is None:
            raise NotFoundException(f"该工具{tool_name}不存在")

        provider_entity = provider.provider_entity
        tool = provider.get_tool_entity(tool_name)

        builtin_tool = {
            "provider": {**provider_entity.model_dump(exclude={"icon", "created_at"})},
            **tool_entity.model_dump(),
            "created_at": provider_entity.created_at,
            "inputs": self.get_tool_inputs(tool),
        }
        return builtin_tool

    def get_provider_icon(self, provider_name: str)-> tuple[bytes, str]:
        provider = self.builtin_provider_manager.get_provider(provider_name)
        if provider is None:
            raise NotFoundException(f"该提供商{provider_name}不存在")

        icon = provider.provider_entity.icon
        if icon is None:
            raise NotFoundException("该提供商没有设置图标")

        root_path = os.path.dirname(os.path.dirname(current_app.root_path))
        provider_path = os.path.join(root_path, "internal", "core", "tool", "builtin_tool", "provider", provider_name)
        icon_path = os.path.join(provider_path, "_asset", icon)

        if not os.path.exists(icon_path):
            raise NotFoundException(f"该提供商{provider_name}的图标{icon}不存在")

        icon_type, _ = mimetypes.guess_type(icon_path)
        icon_type = icon_type or "application/octet-stream"
        with open(icon_path, "rb") as f:
            byte_data = f.read()

        return byte_data, icon_type

    def get_provider_categories(self) -> list[str]:
        provider_entities = self.builtin_provider_manager.get_provider_entities()
        return [provider_entity.category for provider_entity in provider_entities]

    @staticmethod
    def get_tool_inputs(tool) -> list:
        inputs = []
        if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):

            for field_name, model_field in tool.args_schema.model_fields.items():
                inputs.append({
                    "name": field_name,
                    "type": model_field.annotation.__name__,
                    "description": model_field.description or "",
                    "required": model_field.is_required()
                })
        return inputs
