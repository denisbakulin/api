from enum import IntEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, IdMixin, TimeMixin

class User(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "users"

    name: Mapped[str]

    username: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )

    password: Mapped[str] = mapped_column(nullable=True)
    is_active: Mapped[bool] = mapped_column(default=True)

    role: Mapped[UserRoleEnum] = mapped_column(default=UserRoleEnum.USER)




