from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Length, URL, ValidationError

from .schema import ListField


class ValidateOpenAPISchemaReq(FlaskForm):
    """校验open api 规范请求"""
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="openapi_schema字符串不能为空")
    ])


class CreateApiToolReq(FlaskForm):
    name = StringField("name", validators=[
        DataRequired(message="工具提供者名字不能为空"),
        Length(min=1, max=30, message="工具提供者的名字在1-30之间")
    ])
    icon = StringField("icon", validators=[
        DataRequired(message="工具提供者的图标不能为空"),
        URL(message="工具提供者的图标必须是URL链接")
    ])
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="openapi_schema字符串不能为空")
    ])
    headers = ListField("headers")


    @classmethod
    def validate_headers(cls, form, filed):
        """校验headers请求的数据是否正确"""
        for header in filed.data:
            if not isinstance(header, dict):
                raise ValidationError("headers里每一个元素必须是字典")
            if set(header.keys()) != {"key", "value"}:
                raise ValidationError("只能包含key、value这两个属性")
