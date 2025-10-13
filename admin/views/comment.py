from comment.model import Comment
from comment.schemas import CommentShow
from admin.views.base import AdminView

class CommentAdminView(AdminView, model=Comment, delete_=True):
    show = CommentShow

