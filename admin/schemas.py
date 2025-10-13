from pydantic import BaseModel, EmailStr, Field, field_validator

from user.model import UserRoleEnum
from user.schemas import UserCreate, UserShow, UserShowMe


class AdminUserUpdate(UserShow):

    username: str | None = None
    email: EmailStr | None = None


class UserRole(BaseModel):
    role: int










