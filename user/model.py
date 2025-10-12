from sqlalchemy import Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, IdMixin, TimeMixin


class Profile(BaseORM, IdMixin):
    __tablename__ = "profiles"

    bio: Mapped[str | None]
    age: Mapped[int | None]
    city: Mapped[str | None]
    foreign_link: Mapped[str | None]


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)

    user: Mapped["User"] = relationship(back_populates="profile")


class Settings(BaseORM, IdMixin):
    __tablename__ = "user_settings"

    show_in_search: Mapped[bool] = mapped_column(default=True)

    direct_notifications: Mapped[bool] = mapped_column(default=True)
    reaction_notifications: Mapped[bool] = mapped_column(default=True)
    comment_notifications: Mapped[bool] = mapped_column(default=True)
    subscribe_notifications: Mapped[bool] = mapped_column(default=True)

    is_profile_public: Mapped[bool] = mapped_column(default=True)
    enable_direct: Mapped[bool] = mapped_column(default=True)


    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True)
    user: Mapped["User"] = relationship(back_populates="settings")



from uuid import uuid4
class User(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "users"

    depends = [("profile", Profile), ("settings", Settings)]

    tg_id: Mapped[int | None]
    username: Mapped[str] = mapped_column(
        nullable=False, unique=True
    )
    password: Mapped[str] = mapped_column(nullable=True)
    email: Mapped[str] = mapped_column(nullable=True, unique=True)

    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    is_admin: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def password_login(self):
        return bool(self.password)

    profile: Mapped["Profile"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )

    settings: Mapped["Settings"] = relationship(
        back_populates="user",
        uselist=False,
        cascade="all, delete-orphan",
        lazy="joined"
    )



