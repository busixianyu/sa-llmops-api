from typing import Type, Optional

import requests
from injector import inject
from dataclasses import dataclass
from pydantic import BaseModel, create_model, Field
from internal.core.tool.api_tool.entity import ToolEntity, ParameterTypeMap, ParameterIn
from langchain_core.tools import BaseTool, StructuredTool


@inject
@dataclass
class ApiProviderManager(BaseModel):

    @classmethod
    def _create_tool_func_from_tool_entity(cls, tool_entity: ToolEntity):
        def tool_func(**kwargs) -> str:
            """API工具请求函数"""
            # 1.定义变量存储来自path/query/header/cookie/request_body中的数据
            parameters = {
                ParameterIn.PATH: {},
                ParameterIn.QUERY: {},
                ParameterIn.HEADER: {},
                ParameterIn.COOKIE: {},
                ParameterIn.REQUEST_BODY: {}
            }
            # 2.更改参数结构映射
            parameter_map = {
                parameter.get("name"): parameter for parameter in tool_entity.parameters
            }
            header_map = {header.get("key"): header.get("value") for header in tool_entity.headers}
            for key, value in kwargs.items():
                parameter = parameter_map.get(key)
                if parameter is None:
                    continue
                parameters[parameter.get("in", ParameterIn.QUERY)][key] = value
            return requests.request(
                method=tool_entity.method,
                url=tool_entity.url.format(**parameters[ParameterIn.PATH]),
                headers={**header_map, **parameters[ParameterIn.HEADER]},
                params=parameters[ParameterIn.QUERY],
                json=parameters[ParameterIn.REQUEST_BODY],
                cookies=parameters[ParameterIn.COOKIE]
            ).text


        return tool_func

    @classmethod
    def _create_model_from_parameters(cls, parameters: list[dict]) -> Type[BaseModel]:
        fields = {}
        for parameter in parameters:
            field_name = parameter.get("name")
            field_type = ParameterTypeMap.get(parameter.get("type"), str)
            field_required = parameter.get("required", True)
            field_description = parameter.get("description", "")
            fields[field_name] = (
                field_type if field_required else Optional[field_type],
                Field(description=field_description)
            )
        return create_model("DynamicModel", **fields)



    def get_tool(self, tool_entity: ToolEntity):
        return StructuredTool.from_function(
            func=self._create_tool_func_from_tool_entity(tool_entity),
            name=f"{tool_entity.id}_{tool_entity.name}",
            description=tool_entity.description,
            args_schema=self._create_model_from_parameters(tool_entity.parameters)
        )
