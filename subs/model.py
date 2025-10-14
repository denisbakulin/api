from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, TimeMixin


class Subscribe(BaseORM, TimeMixin):
    __tablename__ = "user_subscribes"

    creator_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    subscriber_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    creator: Mapped["User"] = relationship(
        "User",
        foreign_keys=[creator_id],
        lazy="selectin"
    )

    subscriber: Mapped["User"] = relationship(
        "User",
        foreign_keys=[subscriber_id]
    )







