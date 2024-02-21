from contextlib import AbstractAsyncContextManager
from typing import Callable

from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.user import User
from app.errors import exceptions as ex


class LoginRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def post_login_repository(self, user_info: OAuth2PasswordRequestForm) -> dict | None:
        """
        로그인 Repository
        :param user_info: 유저정보
        """
        try:
            async with self.session_factory() as session:
                result = await session.scalars(select(User).where(User.login_id == user_info.username))
                user = result.first()
                if not user:
                    return None
                return {
                    "user_id": user.user_id,
                    "user_password": user.user_password,
                    "login_id": user.login_id,
                    "user_name": user.user_name,
                    "user_email": user.user_email,
                }
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)
