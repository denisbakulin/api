from functools import lru_cache
from os import getenv
from typing import Literal, Self

from pydantic import EmailStr
from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        mode = getenv("MODE", "TEST")
        env_file = ".env" if mode == "DEV" else ".env.test"
        extra = "ignore"


class AppSettings(BaseConfig):
    app_mode: Literal["DEV", "TEST"]
    app_name: str
    db_uri: str


class JWTAuthSettings(BaseConfig):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    class Config(BaseConfig.Config):
        env_prefix = "JWT_"


class TGAuthSettings(BaseConfig):
    token: str

    class Config(BaseConfig.Config):
        env_prefix = "TG_"



class SuperAdminSettings(BaseConfig):
    username: str
    password: str
    email: EmailStr

    class Config(BaseConfig.Config):
        env_prefix = "SUPER_ADMIN_"


class AnonUserSettings(BaseConfig):
    username: str
    password: str

    class Config(BaseConfig.Config):
        env_prefix = "ANON_"


app_settings = AppSettings()
jwt_auth_settings = JWTAuthSettings()
tg_auth_settings = TGAuthSettings()
super_admin_settings = SuperAdminSettings()
anon_settings = AnonUserSettings()




