import os

from flask import Flask
from flask_migrate import Migrate

from pkg.sqlalchemy import SQLAlchemy

from internal.exception import CustomException
from internal.router import Router
from config import Config
from pkg.response import HttpCode
from pkg.response import Response, json
from flask_cors import CORS


class Http(Flask):
    def __init__(self,
                 *args,
                 config: Config,
                 db: SQLAlchemy,
                 migrate: Migrate,
                 router: Router,
                 **kwargs):
        super().__init__(*args, **kwargs)
        self.config.from_object(config)
        self.register_error_handler(Exception, self._register_error_handler)
        db.init_app(self)
        migrate.init_app(self, db, directory="internal/migrations")
        # with self.app_context():
        #     _ = App()
        #     db.create_all()

        # 解决跨域问题
        CORS(self, resources={
            r"/*": {
                "origins": "*",
                "supports_credentials": True,
                # "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
                # "expose_headers": ["Content-Type"]
            }
        })
        router.register_router(self)

    def _register_error_handler(self, error: Exception):
        if isinstance(error, CustomException):
            return json(Response(code=error.code, message=error.message, data=error.data if error.data is not None else {}))
        if self.debug or os.getenv("FLASK_ENV") == "development":
            raise error
        else:
            return json(Response(code=HttpCode.FAIL, message=str(error), data={}))
