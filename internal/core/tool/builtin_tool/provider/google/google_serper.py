from langchain_community.tools import GoogleSerperRun
from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field


class GoogleSerperArgsSchema(BaseModel):
    """谷歌 Serper API 搜索参数描述"""
    query: str = Field(description="需要检索查询的语句")


def google_serper(**kwargs) -> BaseTool:
    """Google 搜索引擎, 用于搜索信息, 重磅更新, 搜索能力更强"""
    return GoogleSerperRun(
        name="google_serper",
        description="Google 搜索引擎, 用于搜索信息, 重磅更新, 搜索能力更强",
        args_schema=GoogleSerperArgsSchema,
        api_wrapper=GoogleSerperAPIWrapper(),
    )