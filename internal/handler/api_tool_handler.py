from uuid import UUID

from injector import inject
from dataclasses import dataclass
from internal.schema.api_tool_schema import (
    ValidateOpenAPISchemaReq,
    CreateApiToolReq,
    GetApiToolProviderResp,
    GetApiToolResp
)
from pkg.response import validate_error_json, success_json, success_message
from internal.service import ApiToolService


@inject
@dataclass
class ApiToolHandler:
    """自定义API插件处理器"""
    api_tool_service: ApiToolService

    def create_api_tool(self):
        """创建自定义api工具"""
        req = CreateApiToolReq()
        if not req.validate():
            return validate_error_json(req.errors)

        self.api_tool_service.create_api_tool(req)
        return success_json("创建自定义API插件成功")


    def get_api_tool_provider(self, provider_id: UUID):
        api_tool_provider = self.api_tool_service.get_api_tool_provider(provider_id)
        resp = GetApiToolProviderResp()
        return success_json(resp.dump(api_tool_provider))

    def get_api_tool(self, provider_id:UUID, tool_name: str):
        api_tool = self.api_tool_service.get_api_tool(provider_id, tool_name)
        resp = GetApiToolResp()
        return success_json(resp.dump(api_tool))

    def delete_api_tool_provider(self, provider_id:UUID):
        self.api_tool_service.delete_api_tool_provider(provider_id)
        return success_message("删除自定义插件成功")

    def validate_openapi_schema(self):
        """验证openapi字符串是否正确"""
        req = ValidateOpenAPISchemaReq()
        if not req.validate():
            return validate_error_json(req.errors)

        self.api_tool_service.parse_openai_schema(req.openapi_schema.data)
        return success_json("数据校验成功")
