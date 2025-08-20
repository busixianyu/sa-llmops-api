from dataclasses import dataclass
from injector import inject
from pydantic import BaseModel

from internal.core.tool.builtin_tool.provider import BuiltinProviderManager


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
                **provider_entity.model_dump(exclude=["icon"]),
                "tools": []
            }

            for tool_entity in provider.get_tool_entities():
                tool_dict = {**tool_entity.model_dump(), "inputs": []}
                tool = provider.get_tool(tool_entity.name)
                if hasattr(tool, "args_schema") and issubclass(tool.args_schema, BaseModel):
                    inputs = []
                    for field_name, model_field in tool.args_schema.model_fields.items():
                        inputs.append({
                            "name": field_name,
                            "type": model_field.annotation.__name__,
                            "description": model_field.description or "",
                            "required": model_field.default_factory is not None,
                        })
                    tool_dict["inputs"] = inputs
                builtin_tool["tools"].append(tool_dict)

            builtin_tools.append(builtin_tool)
        return builtin_tools




    def get_provider_tool(self, provider_name:str, tool_name:str) -> dict:
        return self.builtin_provider_manager.get_tool(provider_name, tool_name)