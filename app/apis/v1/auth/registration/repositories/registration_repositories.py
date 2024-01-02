from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.user import User
from app.errors import exceptions as ex
from app.models.user import UserRegister


class RegistrationRepository:
    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def post_register_repository(self, user_info: UserRegister) -> str | None:
        """
        회원가입 Repository
        :param user_info: 유저정보
        :return:
        """
        try:
            async with self.session_factory() as session:
                if user := await session.scalars(insert(User).values(**user_info.dict()).returning(User)):
                    user_id = user.first().user_id
                    return user_id
                else:
                    return None
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)

    async def check_user(self, user_info: UserRegister):
        """
        아이디, 이메일 중복체크 Repository
        :param user_info: 유저정보
        :return:
        """
        try:
            async with self.session_factory() as session:
                result = await session.scalars(select(User).where(User.user_id == user_info.user_id))
                user = result.first()
                if user is None:
                    return True
                else:
                    raise ex.DuplicateUserEx(user_id=user_info.user_id)
        except SQLAlchemyError as e:
            raise ex.InternalSqlEx(ex=e)
