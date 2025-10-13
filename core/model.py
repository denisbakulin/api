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


    depends: Optional[list[tuple[str, Type["BaseORM"]]]] = None
    """depends = [("profile", Profile), ...]
    создает поля (связанные таблицы) при создании записи 
    """


    def __init__(self, **kwargs):
        if self.depends is not None:
            for dep_name, dep in self.depends:
                setattr(self, dep_name, dep())

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

        super().__init__()

    @classmethod
    def table_info(cls) -> list[ColumnProps]:
        """Возвращает информацию о таблице построчно"""

        inspector = inspect(cls)

        return [
            ColumnProps(
                name=column.name,
                type=str(column.type),
                nullable=bool(column.nullable),
                primary_key=bool(column.primary_key),
                unique=bool(column.unique),
                foreign_key=cls._get_foreign_key_info(column)
            ) for column in inspector.mapper.columns
        ]
    
    @staticmethod
    def _get_foreign_key_info(column) -> Optional[str]:

        foreign_key_info = None
        if column.foreign_keys:
            fk = list(column.foreign_keys)[0]
            foreign_key_info = f"{fk.column.table.name}.{fk.column.name}"
        return foreign_key_info


class IdMixin(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimeMixin(DeclarativeBase):
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)

