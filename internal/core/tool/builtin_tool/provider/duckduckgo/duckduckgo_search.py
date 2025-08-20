from langchain_community.tools import DuckDuckGoSearchRun
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class DDGInput(BaseModel):
    """DuckDuckGo API 搜索参数描述"""
    query: str = Field(description="需要检索查询的语句")


def duckduckgo_search(**kwargs) -> BaseTool:
    """DuckDuckGo 搜索引擎, 用于搜索信息, 重磅更新, 搜索能力更强"""
    return DuckDuckGoSearchRun(
        description="DuckDuckGo 搜索引擎, 用于搜索信息, 搜索能力更强",
        args_schema=DDGInput
    )