from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.user import User
from app.errors import exceptions as ex
from app.models.user import UserBase


class LoginRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def post_login_repository(self, user_info: UserBase) -> dict | None:
        """
        로그인 Repository
        :param user_info: 유저정보
        """
        try:
            async with self.session_factory() as session:
                result = await session.scalars(select(User).where(User.user_id == user_info.user_id))
                user = result.first()
                if user is None:
                    return None
                return {
                    "user_password": user.user_password,
                    "user_id": user.user_id,
                    "user_name": user.user_name,
                    "user_email": user.user_email,
                }
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)
