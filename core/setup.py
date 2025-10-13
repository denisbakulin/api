from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "http://127.0.0.1:5173",
]


def create_app():
    app = FastAPI(lifespan=lifespan, debug=True)
    set_middlewares(app)
    return app


def set_middlewares(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from core.log import LoggingMiddleware
    app.add_middleware(LoggingMiddleware)

    from core.exceptions_middleware import AppExceptionMiddleware
    app.add_middleware(AppExceptionMiddleware)




def include_routers(app: FastAPI):
    from admin.views import admin_router
    from auth.views import auth_router
    from comment.views import comm_router
    from direct.views import direct_router
    from direct.ws import ws
    from integrations.crypto.views import crypto_router
    from integrations.weather.views import weather_router
    from post.views import post_router
    from subs.views import subs_router
    from topic.views import topic_router
    from user.views.me import me_router
    from user.views.other import user_router

    routers: list[APIRouter] = [
        auth_router, user_router,
        me_router, topic_router,
        post_router, comm_router,
        crypto_router, weather_router,
        direct_router, ws, subs_router,
        admin_router
    ]


    for router in routers:
        app.include_router(router)


async def init_db(app: FastAPI):
    from core.db import init_models, session_factory

    await init_models()

    from user.schemas import UserCreate

    from admin.service import AdminUserService
    from core.settings import anon_settings, super_admin_settings
    from topic.service import TopicService


    async with session_factory() as session:
        user_service = AdminUserService(session=session)
        topic_service = TopicService(session=session)

        await user_service.create_super_admin(
            UserCreate(**super_admin_settings.dict())
        )

        anon = await user_service.create_anon(
            UserCreate(**anon_settings.dict())
        )

        await topic_service.create_news_topic(
            anon
        )





@asynccontextmanager
async def lifespan(
        app: FastAPI,
):
    include_routers(app)

    from fastapi_cache import FastAPICache
    from fastapi_cache.backends.redis import RedisBackend
    from redis import asyncio as aioredis

    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")

    await init_db(app)

    yield


