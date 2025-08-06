import uuid
from dataclasses import dataclass

from pkg.sqlalchemy import SQLAlchemy
from injector import inject
from internal.model import App

@inject
@dataclass
class AppService:
    """应用服务类"""
    db: SQLAlchemy

    def create_app(self) -> App:
        with self.db.auto_commit():
            app = App()
            app.name = "测试机器人"
            app.icon = ""
            app.account_id = uuid.uuid4()
            app.description = "用于测试"
            self.db.session.add(app)
        return app

    def get_app(self, id: uuid.UUID) -> App:
        return self.db.session.query(App).get(id)

    def update_app(self, id:uuid.UUID) -> App:
        with self.db.auto_commit():
            app_need_update = self.get_app(id)
            app_need_update.name = "新的机器人"
        return app_need_update

    def delete_app(self, id:uuid.UUID) -> bool:
        with self.db.auto_commit():
            app_need_delete = self.get_app(id)
            self.db.session.delete(app_need_delete)
        return True