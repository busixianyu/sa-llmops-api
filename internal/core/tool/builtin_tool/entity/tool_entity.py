from typing import Any, Optional
from enum import Enum
from pydantic import BaseModel, Field


class ToolParamType(Enum):
    TEXT = "text"
    NUMBER = "number"
    BOOLEAN = "boolean"
    SELECT = "select"

class ToolParam(BaseModel):
    """工具参数类型"""
    name: str = Field(description="参数名称")
    label: str = Field(description="参数展示的标签")
    type: ToolParamType = Field(description="参数类型")
    default: Any = Field(description="参数默认值", default=None)
    required: bool = Field(description="参数是否必填", default=True)
    min: Optional[float] = Field(description="参数最小值", default=None)
    max: Optional[float] = Field(description="参数最大值", default=None)
    options: list[dict[str, Any]] = Field(description="参数选项", default_factory=list)

class ToolEntity(BaseModel):
    """工具实体类，存储的信息映射的是工具名.yaml里的数据"""
    name: str = Field(description="服务名称")
    label: str = Field(description="服务标签")
    description: str = Field(description="服务描述")
    params: list[ToolParam] = Field(description="服务参数", default_factory=list)