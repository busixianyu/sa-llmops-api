from flask import Flask, Blueprint
from internal.handler import AppHandler, BuiltinToolHandler, ApiToolHandler
from injector import inject
from dataclasses import dataclass

@inject
@dataclass
class Router:
    """路由"""

    app_handler: AppHandler
    builtin_tool_handler: BuiltinToolHandler
    api_tool_handler: ApiToolHandler


    def register_router(self, app: Flask):
        # 1.创建一个蓝图
        bp = Blueprint('llmops', __name__, url_prefix="")
        # 2.将url与控制器方法绑定
        bp.add_url_rule("/ping", methods=["GET"],view_func=self.app_handler.ping)
        bp.add_url_rule("/app/<uuid:app_id>/debug", methods=["POST"],view_func=self.app_handler.debug)
        bp.add_url_rule("/app/create", methods=["POST"],view_func=self.app_handler.create_app)
        bp.add_url_rule("/app/<uuid:id>", methods=["GET"],view_func=self.app_handler.get_app)
        bp.add_url_rule("/app/<uuid:id>", methods=["PUT"],view_func=self.app_handler.update_app)
        bp.add_url_rule("/app/<uuid:id>", methods=["DELETE"],view_func=self.app_handler.delete_app)

        # 内置插件
        bp.add_url_rule("/builtin-tool", methods=["GET"], view_func=self.builtin_tool_handler.get_builtin_tools)
        bp.add_url_rule("/builtin-tool/<string:provider_name>/tool/<string:tool_name>", methods=["GET"], view_func=self.builtin_tool_handler.get_provider_tool)
        bp.add_url_rule(
            "/builtin-tool/<string:provider_name>/icon",
            methods=["GET"],
            view_func=self.builtin_tool_handler.get_provider_icon
        )
        bp.add_url_rule(
            "/builtin-tool/categories",
            methods=["GET"],
            view_func=self.builtin_tool_handler.get_provider_categories
        )

        bp.add_url_rule(
            "/api-tool/validate-openapi-schema",
            methods=["POST"],
            view_func=self.api_tool_handler.validate_openapi_schema
        )

        bp.add_url_rule(
            "/api-tool",
            methods=["POST"],
            view_func=self.api_tool_handler.create_api_tool
        )

        bp.add_url_rule(
            "/api-tool/<uuid:provider_id>",
            methods=["GET"],
            view_func=self.api_tool_handler.get_api_tool_provider
        )

        bp.add_url_rule(
            "/api-tool/<uuid:provider_id>/tools/<string:tool_name>",
            methods=["GET"],
            view_func=self.api_tool_handler.get_api_tool
        )

        bp.add_url_rule(
            "/api-tool/<uuid:provider_id>/tools/<string:tool_name>",
            methods=["POST"],
            view_func=self.api_tool_handler.delete_api_tool_provider
        )

        bp.add_url_rule(
            "/api-tool/page",
            methods=["GET"],
            view_func=self.api_tool_handler.get_api_tool_providers_with_page
        )

        bp.add_url_rule(
            "/api-tool/<uuid:provider_id>",
            methods=["POST"],
            view_func=self.api_tool_handler.update_api_tool_provider
        )

        # 3.在应用上注册蓝图
        app.register_blueprint(bp)
