from sqlalchemy.ext.asyncio import AsyncSession

from auth.exceptions import InvalidPasswordError
from auth.schemas import AuthCreds, LoginTokens
from auth.utils import TokenCreator, check_telegram_auth
from user.service import UserService
from user.utils import verify_password


class AuthService:

    def __init__(self, session: AsyncSession):
        self.session = session
        self.user_service = UserService(session=session)


    async def login_via_password(self, creds: AuthCreds) -> LoginTokens:
        user = await self.user_service.get_user_by_username(creds.username)

        if not user.password_login or not \
            verify_password(creds.password, user.password):

            raise InvalidPasswordError()

        return self._create_auth_tokens(user.id)


    async def login_via_telegram(self, initData: str) -> LoginTokens:

        user = check_telegram_auth(initData)

        user = await self.user_service.login_user_via_telegram(user)

        return self._create_auth_tokens(user.id)


    def _create_auth_tokens(self, user_id: int) -> LoginTokens:
        tokens = TokenCreator(user_id)

        return LoginTokens(
            access_token=tokens.access,
            refresh_token=tokens.refresh
        )














