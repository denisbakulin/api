from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, TimeMixin, IdMixin


class Reaction(BaseORM, TimeMixin, IdMixin):
    __tablename__ = "user_reactions"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    post_id: Mapped[int | None] = mapped_column(
        ForeignKey("posts.id", ondelete="CASCADE")
    )
    topic_id: Mapped[int | None] = mapped_column(
        ForeignKey("topics.id", ondelete="CASCADE")
    )

    post: Mapped["Post"] = relationship("Post", lazy="selectin")
    topic: Mapped["Topic"] = relationship("Topic", lazy="selectin")
    user: Mapped["User"] = relationship("User", lazy="selectin")



    reaction: Mapped[str] = mapped_column(nullable=False)





