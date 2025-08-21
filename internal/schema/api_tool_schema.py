from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class ValidateOpenAPISchema(FlaskForm):
    """校验open api 规范请求"""
    openapi_schema = StringField("openapi_schema", validators=[
        DataRequired(message="openapi_schema字符串不能为空")
    ])