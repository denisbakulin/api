from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import InvalidPasswordError
from auth.schemas import AuthCreds, LoginTokens
from auth.utils import TokenCreator
from user.service import UserService
from user.utils import verify_password

from auth.utils import check_telegram_auth



class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)


    async def login_via_password(self, creds: AuthCreds) -> LoginTokens:
        user = await self.user_service.get_user_by_username(creds.username)

        if not user.password_login or not \
            verify_password(creds.password, user.password):

            raise InvalidPasswordError()

        tokens = TokenCreator(user.id)

        return LoginTokens(
            access_token=tokens.access,
            refresh_token=tokens.refresh
        )


    async def login_via_telegram(self, initData: str) -> LoginTokens:

        user = check_telegram_auth(initData)

        user = await self.user_service.login_user_via_telegram(user)

        tokens = TokenCreator(user.id)

        return LoginTokens(
            access_token=tokens.access,
            refresh_token=tokens.refresh
        )













