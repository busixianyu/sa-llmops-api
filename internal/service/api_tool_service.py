import json
from typing import Any
from uuid import UUID
from sqlalchemy import desc
from injector import inject
from dataclasses import dataclass
from pkg.paginator import Paginator
from internal.core.tool.api_tool.entity import OpenAPISchema
from internal.exception import ValidateErrorException, NotFoundException
from internal.schema.api_tool_schema import (
    CreateApiToolReq,
    GetApiToolProvidersWithPageReq, UpdateApiToolProviderReq
)
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

    def get_api_tool_provider(self, provider_id: UUID) -> ApiToolProvider:
        # TODO 获取账号信息
        account_id = ""
        api_tool_provider = self.db.session.query(ApiToolProvider).get(provider_id)
        if api_tool_provider is None or str(api_tool_provider.account_id) != account_id:
            raise NotFoundException("工具提供者不存在")

        return api_tool_provider

    def get_api_tool(self, provider_id: UUID, tool_name: str) -> ApiTool:
        # todo 获取账号
        account_id = ""
        api_tool = self.db.session.query(ApiTool).filter_by(
            provider_id=provider_id,
            name=tool_name
        ).one_or_none()
        if api_tool is None or str(api_tool.account_id) != account_id:
            raise NotFoundException("该工具不存在")
        return api_tool

    def delete_api_tool_provider(self, provider_id: UUID):
        # todo 获取账号
        account_id = ""
        provider = self.get_api_tool_provider(provider_id)
        with self.db.auto_commit():
            self.db.session.query(ApiTool).filter(
                ApiTool.provider_id == provider_id,
                ApiTool.account_id == account_id
            ).delete()
            self.db.session.delete(provider)

    def get_api_tool_providers_with_page(self, req: GetApiToolProvidersWithPageReq) -> tuple[list[Any], Paginator]:
        # todo 获取账号
        account_id = ""
        paginator = Paginator(db=self.db, req=req)
        filters = [ApiToolProvider.account_id == account_id]
        if req.search_word.data:
            filters.append(ApiToolProvider.name.ilike(f"%{req.search_word.data}%"))

        api_tool_providers = paginator.paginate(
            self.db.session.query(ApiToolProvider).filter(*filters).order_by(desc("created_at"))
        )
        return api_tool_providers, paginator

    def update_api_tool_provider(self, provider_id:UUID, req:UpdateApiToolProviderReq):
        # todo 获取账号
        account_id = ""
        api_tool_provider = self.get_api_tool_provider(provider_id)
        openapi_schema = self.parse_openai_schema(req.openapi_schema.data)
        check_api_tool_provider = self.db.session.query(ApiToolProvider).filter(
            ApiToolProvider.account_id==account_id,
            ApiToolProvider.name==req.name.data,
            ApiToolProvider.id!=api_tool_provider.id
        ).one_or_none()
        if check_api_tool_provider:
            raise ValidateErrorException(f"该工具提供者名字{req.name.data}已存在")
        with self.db.auto_commit():
            self.db.session.query(ApiTool).filter(
                ApiTool.provider_id==api_tool_provider.id,
                ApiTool.account_id==account_id
            ).delete()
            api_tool_provider.name= req.name.data
            api_tool_provider.icon=req.icon.data
            api_tool_provider.headers=req.headers.data
            api_tool_provider.openapi_schema=req.openapi_schema.data

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

