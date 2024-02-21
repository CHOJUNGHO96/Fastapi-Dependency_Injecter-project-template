from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.user import User
from app.errors import exceptions as ex
from app.models.user import ModelUserRegister


class RegistrationRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def post_register_repository(self, user_info: ModelUserRegister) -> bool:
        """
        회원가입 Repository
        :param user_info: 유저정보
        """
        try:
            async with self.session_factory() as session:
                if await session.scalars(insert(User).values(**user_info.dict()).returning(User)):
                    return True
                else:
                    return False
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)

    async def check_user(self, user_info: ModelUserRegister):
        """
        아이디, 이메일 중복체크 Repository
        :param user_info: 유저정보
        """
        try:
            async with self.session_factory() as session:
                result = await session.scalars(select(User).where(User.login_id == user_info.login_id))
                user = result.first()
                if user is None:
                    return True
                else:
                    raise ex.DuplicateUserEx(user_id=user_info.login_id)
        except SQLAlchemyError as e:
            raise ex.InternalSqlEx(ex=e)
