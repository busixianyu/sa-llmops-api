import os.path
from typing import Any
import yaml
from injector import inject, singleton
from internal.core.tool.builtin_tool.entity import ProviderEntity, Provider


@inject
@singleton
class BuiltinProviderManager:
    """服务提供商工厂类"""
    provider_map: dict[str, Provider] = {}

    def __init__(self) -> None:
        self._get_provider_tool_map()

    def get_provider(self, provider_name: str) -> Provider:
        return self.provider_map.get(provider_name)

    def get_providers(self) -> list[Provider]:
        return list(self.provider_map.values())

    def get_provider_entities(self) -> list[ProviderEntity]:
        return [provider.provider_entity for provider in self.get_providers()]

    def get_tool(self, provider_name:str, tool_name:str) -> Any:
        provider = self.get_provider(provider_name)
        if provider is None:
            return None
        return provider.get_tool(tool_name)

    def _get_provider_tool_map(self):
        """项目初始化的时候获取服务提供商工具映射关系"""
        if self.provider_map:
            return

        # 获取当前文件/类路径
        current_path = os.path.abspath(__file__)
        provider_path = os.path.dirname(current_path)
        provider_yaml_path = os.path.join(provider_path, "provider.yaml")

        # 读取yaml文件
        with open(provider_yaml_path, 'r', encoding='utf-8') as f:
            provider_yaml_data = yaml.safe_load(f)

        # 循环遍历yaml数据
        for idx, provider_data in enumerate(provider_yaml_data):
            provider_entity = ProviderEntity(**provider_data)
            self.provider_map[provider_entity.name] = Provider(
                name=provider_entity.name,
                position=idx + 1,
                provider_entity=provider_entity
            )
