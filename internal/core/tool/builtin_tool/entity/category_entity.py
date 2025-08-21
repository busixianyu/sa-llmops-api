from pydantic import BaseModel, Field, field_validator
from internal.exception import FailException


class CategoryEntity(BaseModel):
    """分类实体"""
    category: str = Field(description="分类唯一标识")
    name: str = Field(description="分类名称")
    icon: str = Field(description="分类图标")

    @field_validator("icon")
    def check_icon(cls, value: str):
        if not value.endswith("svg"):
            raise FailException("icon must be svg file")
        return value