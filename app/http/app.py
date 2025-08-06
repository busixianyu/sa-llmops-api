from pkg.sqlalchemy import SQLAlchemy
from injector import Injector
from .module import ExtensionModule
from config import Config
from internal.router import Router
from internal.server import Http
from flask_migrate import Migrate

injector = Injector([ExtensionModule])
conf = Config()

app = Http(__name__,
           config=conf,
           db=injector.get(SQLAlchemy),
           migrate=injector.get(Migrate),
           router=injector.get(Router)
           )

if __name__ == '__main__':
    app.run(debug=True)
