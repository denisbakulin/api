from enum import StrEnum

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, IdMixin, TimeMixin


class TopicOfferStatus(StrEnum):
    PENDING = "pending"
    APPROVE = "approve"
    REJECT = "reject"



class Topic(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "topics"

    title: Mapped[str]
    slug: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    description: Mapped[str | None]

    approved_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    suggested_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)

    suggested_by_user: Mapped["User"] = relationship(
        "User", foreign_keys=[suggested_user_id], lazy="selectin"
    )
    approved_user: Mapped["User"] = relationship(
        "User", foreign_keys=[approved_user_id], lazy="selectin"
    )



class TopicOffer(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "topic_offers"

    title: Mapped[str]
    description: Mapped[str | None]
    status: Mapped[TopicOfferStatus] = mapped_column(default=TopicOfferStatus.PENDING)


    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    process_user_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"), nullable=True)


    author: Mapped["User"] = relationship(
        "User", lazy="selectin", foreign_keys=[author_id]
    )


    process_user: Mapped["User"] = relationship(
        "User", lazy="selectin", foreign_keys=[process_user_id]
    )









