from typing import Optional, Union

from fastapi import Depends, Request
from fastapi_users import (
    BaseUserManager,
    FastAPIUsers,
    IntegerIDMixin,
    InvalidPasswordException,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.db import get_async_session
from app.models.user import User
from app.schemas.user import UserCreate


MIN_PASS_LEN = 3


async def get_user_db(
    session: AsyncSession = Depends(get_async_session),
) -> SQLAlchemyUserDatabase:
    yield SQLAlchemyUserDatabase(session, User)


bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.secret, lifetime_seconds=settings.token_lifetime
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    async def validate_password(
        self,
        password: str,
        user: Union[UserCreate, User],
    ) -> None:
        if len(password) < MIN_PASS_LEN:
            raise InvalidPasswordException(
                # С другим текстом не проходит встроенные тесты
                reason=(
                    f"Password should be at least {MIN_PASS_LEN} characters"
                )
            )
        if user.email in password:
            raise InvalidPasswordException(
                reason="Пароль не может сожержать e-mail"
            )

    async def on_after_register(
        self, user: User, request: Optional[Request] = None
    ) -> None:
        print(f"Пользователь {user.email} зарегистрирован.")


async def get_user_manager(
    user_db: SQLAlchemyUserDatabase = Depends(get_user_db),
) -> UserManager:
    yield UserManager(user_db)


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)
current_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)
