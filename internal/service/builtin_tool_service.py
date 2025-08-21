from dataclasses import dataclass
from injector import inject
from pydantic import BaseModel

from internal.core.tool.builtin_tool.provider import BuiltinProviderManager
from internal.exception import NotFoundException


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
            "provider": {**provider_entity.model_dump(exclude={"icon", })},
            **tool_entity.model_dump(),
            "inputs": self.get_tool_inputs(tool),
        }
        return builtin_tool

    @staticmethod
    def get_tool_inputs(tool) -> list:
        inputs = []
        if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):

            for field_name, model_field in tool.args_schema.model_fields.items():
                inputs.append({
                    "name": field_name,
                    "type": model_field.annotation.__name__,
                    "description": model_field.description or "",
                    "required": model_field.default_factory is None,
                })
        return inputs