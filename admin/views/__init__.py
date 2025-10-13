from admin.views.post import PostAdminView
from admin.views.user import UserAdminView
from admin.views.comment import CommentAdminView

from admin.views.base import Admin


admin_router = Admin(
    UserAdminView(table_name="Пользователи"),
    PostAdminView(table_name="Посты"),
    CommentAdminView(table_name="Комментарии")
)
