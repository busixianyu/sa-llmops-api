from pkg.sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from injector import Module, Binder

from internal.extension import db, migrate


class ExtensionModule(Module):
    def configure(self, binder: Binder):
        binder.bind(SQLAlchemy, to=db)
        binder.bind(Migrate, to=migrate)