from sqlalchemy.orm import Mapped, mapped_column,relationship

from core.model import BaseORM, IdMixin, TimeMixin


from sqlalchemy import ForeignKey
class Topic(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "topics"

    title: Mapped[str]
    slug: Mapped[str] = mapped_column(index=True, unique=True, nullable=True)
    description: Mapped[str | None]


class TopicOffer(BaseORM, IdMixin, TimeMixin):
    __tablename__ = "topic_offers"

    title: Mapped[str]
    description: Mapped[str | None]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    status: Mapped[str]  #rejected #pending #approve

    author: Mapped["User"] = relationship("User", lazy="joined")








