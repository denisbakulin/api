from sqlalchemy import ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, IdMixin, TimeMixin


class DirectMessage(BaseORM, TimeMixin, IdMixin):
    __tablename__ = "direct_messages"

    recipient_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    sender_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    content: Mapped[str] = mapped_column(nullable=False)



class DirectChat(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "direct_chats"

    first_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    second_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    first_user = relationship(
        "User",
        foreign_keys=[first_user_id],
    )

    second_user = relationship(
        "User",
        foreign_keys=[second_user_id],
    )

    __table_args__ = (
        UniqueConstraint("first_user_id", "second_user_id", name="uq_direct_chat_users"),
        Index("ix_direct_chat_users", "first_user_id", "second_user_id"),
    )

    def __repr__(self):
        return f"Личный чат [{self.first_user.username} - {self.second_user.username}]"


class DirectUserSettings(BaseORM):
    __tablename__ = "direct_user_settings"

    chat_id: Mapped[int] = mapped_column(ForeignKey("direct_chats.id"), primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)

    chat_name: Mapped[str | None] = mapped_column(nullable=True)












