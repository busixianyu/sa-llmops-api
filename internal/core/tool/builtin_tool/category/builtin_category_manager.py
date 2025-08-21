import os.path
from typing import Any
import yaml
from pydantic import BaseModel, Field
from injector import inject, singleton
from internal.core.tool.builtin_tool.entity.category_entity import CategoryEntity
from internal.exception import FailException


@singleton
@inject
class BuiltinCategoryManager(BaseModel):

    category_map: dict[str, Any] = Field(default_factory=dict)

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)
        self._init_categories()

    def get_category_map(self):
        return self.category_map

    def _init_categories(self):
        """从配置文件中读取category们，并且放入category_map中"""
        if self.category_map:
            return
        current_path = os.path.abspath(__file__)
        category_path = os.path.dirname(current_path)
        category_yaml_path = os.path.join(category_path, "category.yaml")
        with open(category_yaml_path, 'r', encoding='utf-8') as f:
            categories = yaml.safe_load(f)
        for category in categories:
            category_entity = CategoryEntity(**category)
            icon_path = os.path.join(category_path, "icon", category_entity.icon)
            if not os.path.exists(icon_path):
                raise FailException(f"icon :{category_entity.icon} not exists")
            with open(icon_path, "r", encoding="utf-8") as f:
                icon = f.read()

            self.category_map[category_entity.category] = {
                "entity": category_entity,
                "icon": icon,
            }