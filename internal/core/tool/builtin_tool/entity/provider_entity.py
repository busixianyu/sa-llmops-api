import os.path
from typing import Any
import yaml
from pydantic import BaseModel, Field
from internal.lib.helper import dynamic_import

from .tool_entity import ToolEntity


class ProviderEntity(BaseModel):
    """服务提供商实体，映射的数据是provider.yaml里的每条数据"""
    name: str = Field(description="名字")
    label: str = Field(description="标签，前端显示")
    description: str = Field(description="描述")
    icon: str = Field(description="图标地址")
    background: str = Field(description="图标背景色")
    category: str = Field(description="分类")
    created_at: int = Field(description="提供商/工具的创建时间", default=0)


class Provider(BaseModel):
    """服务提供商"""
    name: str = Field(description="名字")
    position: int = Field(description="排序")
    provider_entity: ProviderEntity = Field(description="服务提供商实体")
    tool_entity_map: dict[str, ToolEntity] = Field(description="工具实体映射", default_factory=dict)
    tool_func_map: dict[str, Any] = Field(description="工具函数映射", default_factory=dict)

    def __init__(self, **kwargs: Any):
        super().__init__(**kwargs)
        self._provider_init()

    class Config:
        protected_namespaces = ()

    def get_tool(self, tool_name: str) -> Any:
        """根据工具的名字，来获取到该服务提供商下的工具"""
        return self.tool_func_map[tool_name]

    def get_tool_entity(self, tool_name: str) -> ToolEntity:
        """根据工具的名字，来获取到该服务提供商下的工具实体"""
        return self.tool_entity_map[tool_name]

    def get_tool_entities(self) -> list[ToolEntity]:
        return list(self.tool_entity_map.values())

    def _provider_init(self) -> None:
        """服务提供商初始化函数"""
        # 获取当前类的路径，计算得到对应服务提供商的路径
        current_path = os.path.abspath(__file__)
        entity_path = os.path.dirname(current_path)
        provider_path = os.path.join(os.path.dirname(entity_path), "provider", self.name)

        # 组装position.yaml数据
        with open(os.path.join(provider_path, "position.yaml"), "r", encoding="utf-8") as f:
            position_yaml_data = yaml.safe_load(f)

        # 循环读取位置信息，获取服务提供商的工具名字
        for tool_name in position_yaml_data:
            # 获取工具的yaml数据
            tool_yaml_path = os.path.join(provider_path, f"{tool_name}.yaml")
            with open(tool_yaml_path, "r", encoding="utf-8") as f:
                tool_yaml_data = yaml.safe_load(f)

            # 将工具的yaml数据转换为ToolEntity对象，并添加到工具实体映射中
            self.tool_entity_map[tool_name] = ToolEntity(**tool_yaml_data)

            # 动态导入对应工具并填充到tool_func_map中
            self.tool_func_map[tool_name] = dynamic_import(
                f"internal.core.tool.builtin_tool.provider.{self.name}",
                tool_name,
            )
