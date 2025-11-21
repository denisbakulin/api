from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI

origins = [
    "http://localhost:5173",
]

def create_app():
    app = FastAPI(lifespan=lifespan, debug=True)
    set_middlewares(app)
    return app


def set_middlewares(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware

    origins = ["http://localhost:5173"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    from core.exceptions_middleware import AppExceptionMiddleware
    app.add_middleware(AppExceptionMiddleware)




def include_routers(app: FastAPI):
    from auth.views import auth_router
    from direct.views import direct_router
    from direct.ws import ws
    from user.views import user_router

    routers: list[APIRouter] = [
        auth_router, user_router,
        direct_router, ws
    ]


    for router in routers:
        app.include_router(router)


async def init_db(app: FastAPI):
    from core.db import init_models, session_factory

    await init_models()

    from user.schemas import UserCreate


    from core.settings import super_admin_settings


    async with session_factory() as session:
        from user.service import UserService
        from user.model import UserRoleEnum
        user_service = UserService(session=session)

        try:
            user = await user_service.create_user(
                UserCreate(**super_admin_settings.dict())
            )
            await user_service.update_item(user, role=UserRoleEnum.ADMIN)
        except:
            ...





@asynccontextmanager
async def lifespan(
        app: FastAPI,
):
    include_routers(app)

    await init_db(app)

    yield


