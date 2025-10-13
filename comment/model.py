from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.model import BaseORM, TimeMixin


class Comment(BaseORM, TimeMixin):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True)

    content: Mapped[str] = mapped_column(nullable=False)

    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    parent_id: Mapped[int] = mapped_column(ForeignKey("comments.id", ondelete="CASCADE"), nullable=True)

    post: Mapped["Post"] = relationship("Post", lazy="joined")
    author: Mapped["User"] = relationship("User", lazy="joined")


    parent: Mapped["Comment"] = relationship(
        "Comment",
        remote_side=[id]
    )





