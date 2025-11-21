from datetime import datetime
from typing import Optional, Type

from pydantic import BaseModel, Field
from sqlalchemy import inspect
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class ColumnProps(BaseModel):
    name: str
    type: str
    nullable: bool = Field(default=False)
    primary_key: bool = Field(default=False)
    unique: bool = Field(default=False)
    foreign_key: Optional[str] = Field(default=None)



class BaseORM(DeclarativeBase):
    __abstract__ = True

    def __init__(self, **kwargs):

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        super().__init__()

class IdMixin(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimeMixin(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

