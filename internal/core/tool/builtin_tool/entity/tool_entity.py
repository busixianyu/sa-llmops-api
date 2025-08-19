from typing import Any

from pydantic import BaseModel, Field


class ToolEntity(BaseModel):
    """工具实体类，存储的信息映射的是工具名.yaml里的数据"""
    name: str = Field(description="服务名称")
    label: str = Field(description="服务标签")
    description: str = Field(description="服务描述")
    params: list = Field(description="服务参数", default_factory=list)