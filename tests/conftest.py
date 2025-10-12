from os import getenv

import pytest
from dotenv import load_dotenv

load_dotenv(".env.test")

@pytest.fixture(scope="session", autouse=True)
def ensure_test_env():
    mode = getenv("APP_MODE")
    if mode != "TEST":
        pytest.exit(f"Окружение [{mode}] не подходит для тестирования!", returncode=1)


from auth.utils import TokenCreator
from comment.service import CommentService
from post.service import PostService
from reaction.service import ReactionService
from user.schemas import UserCreate
from user.service import UserService

users = [
    UserCreate(
        username=f"user{i}",
        password="12345",
        email=f"user{i}@example.com"
    )
    for i in range(1, 25)
]


import pytest_asyncio
from httpx import ASGITransport, AsyncClient

from core.db import get_engine
from core.settings import FirstAdminSettings
from core.setup import create_app

pytest_plugins = ['pytest_asyncio']

from core.db import session_factory


@pytest_asyncio.fixture(scope="module", autouse=True)
async def db():
    from core.model import BaseORM

    engine = get_engine()

    yield
    async with engine.begin() as conn:
        await conn.run_sync(BaseORM.metadata.drop_all)
    await engine.dispose()



@pytest_asyncio.fixture(scope="module")
async def client(db):

    app = create_app()

    lifespan_context = app.router.lifespan_context

    async with lifespan_context(app):
        async with AsyncClient(
                transport=ASGITransport(app=app),
                base_url="http://test"
        ) as ac:
            yield ac

@pytest_asyncio.fixture(scope="module", autouse=True)
async def admin_client(client):
    admin_info = FirstAdminSettings()

    response = await client.post(
        "/auth/login",
        json={
            "username": admin_info.username,
            "password": admin_info.password
        }
    )

    access_token = response.json().get("access_token")

    client.headers.update({"Authorization": f"Bearer {access_token}"})

    return client

from random import choice

from comment.schemas import CommentCreate
from post.schemas import PostCreate


@pytest_asyncio.fixture(scope="module", autouse=True)
async def auth_client(client):
    async with session_factory() as session:
        # сервисы
        user_service = UserService(session)
        post_service = PostService(session)
        comment_service = CommentService(session)
        reaction_service = ReactionService(session)

        # создаём тестового пользователя
        user = await user_service.create_user(UserCreate(
            username="test_user",
            password="12345",
            email="test_user@example.com"
        ))

        users = [
            UserCreate(username=f"user{i}", password="12345", email=f"user{i}@test.com")
            for i in range(2)
        ]

        for _user in users:
            _user = await user_service.create_user(_user)

            post = await post_service.create_post(
                user,
                PostCreate(title="test_post", content="интересно")
            )

            await comment_service.create_comment(
                CommentCreate(parent_id=None, content="коммент"),
                _user, post
            )

            await reaction_service.add_reaction(
                _user, post, choice(["like", "dislike", "love"])
            )


        access_token = TokenCreator(user.id).access
        client.headers.update({"Authorization": f"Bearer {access_token}"})
        client.user = user





    return client



