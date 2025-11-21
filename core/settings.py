from pydantic_settings import BaseSettings


class BaseConfig(BaseSettings):
    class Config:
        env_file = ".env"
        extra = "ignore"



class JWTAuthSettings(BaseConfig):
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    refresh_token_expire_days: int

    class Config(BaseConfig.Config):
        env_prefix = "JWT_"



class SuperAdminSettings(BaseConfig):
    username: str
    password: str
    name: str = "Администратор"

    class Config(BaseConfig.Config):
        env_prefix = "SUPER_ADMIN_"



jwt_auth_settings = JWTAuthSettings()
super_admin_settings = SuperAdminSettings()





