from pydantic import EmailStr, Field, field_validator

from core.schemas import BaseSchema, IdMixinSchema, TimeMixinSchema

from user.model import UserRoleEnum


class UserUsername(BaseSchema):
    username: str


class UserCreate(BaseSchema):
    username: str = Field(min_length=1)
    password: str = Field(min_length=5)
    name: str = Field(min_length=1)

    @field_validator("username")
    def normalize_name(cls, username: str):
        return username.strip().lower()


class UserShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    username: str
    name: str
    role: UserRoleEnum
    is_active: bool

