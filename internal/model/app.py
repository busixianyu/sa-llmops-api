import uuid
from datetime import datetime

from internal.extension import db
from sqlalchemy import (
    Column,
    String,
    UUID,
    Text,
    DateTime,
    PrimaryKeyConstraint,
    Index
)


class App(db.Model):
    __tablename__ = 'app'
    __table_args__ = (
        # PrimaryKeyConstraint("id", name="pk_app_id")
        Index("idx_account_id", "account_id"),
    )
    id = Column('id', UUID, default=uuid.uuid4, primary_key=True, nullable=False)
    name = Column('name', String(255), nullable=False, default="")
    account_id = Column(UUID, nullable=False)
    icon = Column(String(255), nullable=False, default="")
    status = Column(String(255), nullable=False, default="")
    description = Column(Text, default="", nullable=False)
    created_at = Column('created_at', DateTime, default=datetime.now, nullable=False)
    updated_at = Column('updated_at', DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)