
DEFAULT_CONFIG = {
    "SQLALCHEMY_DATABASE_URI": "postgresql://postgres:123456@localhost:5432/llmops?client_encoding=utf8",
    "SQLALCHEMY_TRACK_MODIFICATIONS": False,
    "SQLALCHEMY_POOL_SIZE": 30,
    "SQLALCHEMY_POOL_RECYCLE": 3600,
    "SQLALCHEMY_ECHO": True,
    "SECRET_KEY": "secret-key",
    "DEBUG": True,
    "WTF_CSRF_ENABLED": False,
    "TESTING": True
}