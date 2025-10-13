from admin.views.base import AdminView
from post.model import Post
from fastapi import Depends
from post.deps import postDep, postServiceDep
from post.schemas import PostAllows, PostShow, PostUpdate



class PostAdminView(AdminView, model=Post, delete_=True):
    show = PostShow

    def init_custom_views(self):

        @self.patch(
            "/{slug}",
            summary="Изменить пост",
            response_model=self.show
        )
        async def edit_post(
                post: postDep,
                updates: PostUpdate,
                post_service: postServiceDep,
                allows: PostAllows = Depends()
        ):
            return await post_service.update_item(
                post, **updates.dict(), **allows.dict()
            )

