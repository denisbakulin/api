from typing import Optional

from pydantic import EmailStr, Field, field_validator

from core.schemas import BaseSchema,  IdMixinSchema, TimeMixinSchema


class UserCreate(BaseSchema):
    username: str = Field(min_length=1)
    password: str = Field(min_length=5)
    email: EmailStr | None = None


    @field_validator("username")
    def normalize_name(cls, username: str):
        return username.strip().lower()

class UserProfile(BaseSchema):
    bio: str | None = None
    age: int | None = None
    city: str | None = None
    foreign_link: str | None = None


class UserUpdate(BaseSchema):
    username: Optional[str] = Field(default=None)
    email: EmailStr | None = None
    profile: UserProfile | None = None



class PostUserShow(BaseSchema):
    username: str


class UserShow(BaseSchema, IdMixinSchema, TimeMixinSchema):
    username: str
    profile: UserProfile | None
    is_active: bool
    email: str


class UserShowMe(UserShow):
    is_admin: bool
    password_login: bool



class PasswordChange(BaseSchema):

    old_password: str = Field(min_length=5)
    new_password: str = Field(min_length=5)


class PasswordCreate(BaseSchema):
    password: str = Field(min_length=5)




class UserSettings(BaseSchema):

    show_in_search: bool

    direct_notifications: bool
    reaction_notifications: bool
    comment_notifications: bool

    enable_direct: bool
    is_profile_public: bool


