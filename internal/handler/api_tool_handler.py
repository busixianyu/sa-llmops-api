from injector import inject
from dataclasses import dataclass
from internal.schema.api_tool_schema import ValidateOpenAPISchema
from pkg.response import validate_error_json, success_json
from internal.service import ApiToolService


@inject
@dataclass
class ApiToolHandler:
    """自定义API插件处理器"""
    api_tool_service: ApiToolService

    def validate_openapi_schema(self):
        """验证openapi字符串是否正确"""
        req = ValidateOpenAPISchema()
        if not req.validate():
            return validate_error_json(req.errors)

        self.api_tool_service.parse_openai_schema(req.openapi_schema.data)
        return success_json("数据校验成功")

