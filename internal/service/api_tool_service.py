import json
from typing import Any

from injector import inject
from dataclasses import dataclass

from internal.core.tool.api_tool.entity import OpenAPISchema
from internal.exception import ValidateErrorException


@inject
@dataclass
class ApiToolService:

    @classmethod
    def parse_openai_schema(cls, openapi_schema_str: str) -> Any:
        try:
            data = json.loads(openapi_schema_str)
            if not isinstance(data, dict):
                raise
        except Exception as e:
            raise ValidateErrorException("数据不符合OpenAPI格式规范")

        return OpenAPISchema(**data)
