import json
from typing import Any

from injector import inject
from dataclasses import dataclass

from internal.core.tool.api_tool.entity import OpenAPISchema
from internal.exception import ValidateErrorException, NotFoundException
from internal.schema.api_tool_schema import CreateApiToolReq
from pkg.sqlalchemy import SQLAlchemy
from internal.model import ApiToolProvider, ApiTool


@inject
@dataclass
class ApiToolService:
    db: SQLAlchemy

    @classmethod
    def parse_openai_schema(cls, openapi_schema_str: str) -> OpenAPISchema:
        try:
            data = json.loads(openapi_schema_str.strip())
            if not isinstance(data, dict):
                raise
        except Exception as e:
            raise ValidateErrorException("数据不符合OpenAPI格式规范")

        return OpenAPISchema(**data)

    def create_api_tool(self, req: CreateApiToolReq) -> None:
        # todo 授权认证
        account_id = ""
        openapi_schema = self.parse_openai_schema(req.openapi_schema.data)
        api_tool_provider = self.db.session.query(ApiToolProvider).filter_by(
            account_id=account_id,
            name=req.name.data
        ).one_or_none()
        if api_tool_provider:
            raise ValidateErrorException(f"工具提供者名称{req.name.data}已存在")
        with self.db.auto_commit():
            api_tool_provider = ApiToolProvider(
                account_id=account_id,
                name=req.name.data,
                icon=req.icon.data,
                description=openapi_schema.description,
                openapi_schema=req.openapi_schema.data,
                headers=req.headers.data
            )
            self.db.session.add(api_tool_provider)
            self.db.session.flush()

            for path, path_item in openapi_schema.paths.items():
                for method, method_item in path_item.items():
                    api_tool = ApiTool(
                        account_id=account_id,
                        provider_id=api_tool_provider.id,
                        name=method_item.get("operationId"),
                        description=method_item.get("description"),
                        url=f"{openapi_schema.server}{path}",
                        method=method,
                        parameters=method_item.get("parameters", [])
                    )
                    self.db.session.add(api_tool)

    def get_api_tool_provider(self, provider_id) -> ApiToolProvider:
        # TODO 获取账号信息
        account_id = ""
        api_tool_provider = self.db.session.query(ApiToolProvider).get(provider_id)
        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException("工具提供者不存在")

        return api_tool_provider
