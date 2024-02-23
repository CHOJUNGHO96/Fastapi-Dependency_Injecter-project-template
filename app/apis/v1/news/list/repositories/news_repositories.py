from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import delete, insert, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.v1.news.list.sqlalchemy_helper import SqlalchemyHelper
from app.database.schema.news import News
from app.errors import exceptions as ex
from app.models.news import (
    ModelNewsBase,
    ModelNewsDelete,
    ModelNewsPut,
    ModelNewsRegister,
)


class NewsListRepository:
    """
    뉴스 리스트 Repository
    """

    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
        sqlalchemy_helper: SqlalchemyHelper,
    ) -> None:
        self.session_factory = session_factory
        self.sqlalchemy_helper = sqlalchemy_helper

    async def get_news_list_repository(self, news_info: ModelNewsBase) -> list[dict] | list:
        """
        Get Repository
        """
        try:
            async with self.session_factory() as session:
                conditions = await self.sqlalchemy_helper.get_news_list_filter(News, news_info)
                result = await session.scalars(select(News).where(*conditions).order_by(News.article_id.desc()))
                news_list = result.all()
                if not news_list:
                    return []
                return [
                    {
                        "article_id": news.article_id,
                        "title": news.title,
                        "content": news.content,
                        "source": news.source,
                        "user_id": news.user_id,
                        "url": news.url,
                    }
                    for news in news_list
                ]
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)

    async def post_news_list_repository(self, news_info: ModelNewsRegister) -> list[dict] | list:
        """
        Post Repository
        """
        try:
            async with self.session_factory() as session:
                if result := await session.scalars(insert(News).values(**news_info.dict()).returning(News)):
                    news_list = result.all()
                    return [
                        {
                            "article_id": news.article_id,
                        }
                        for news in news_list
                    ]
                else:
                    return []
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)

    async def put_news_list_repository(self, news_info: ModelNewsPut) -> list[dict] | list:
        """
        Put Repository
        """
        try:
            async with self.session_factory() as session:
                values = {key: value for key, value in news_info.dict().items() if value}
                if result := await session.scalars(
                    update(News).where(News.article_id == news_info.article_id).values(**values).returning(News)
                ):
                    news_list = result.all()
                    return [
                        {
                            "article_id": news.article_id,
                        }
                        for news in news_list
                    ]
                else:
                    return []
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)

    async def delete_news_list_repository(self, news_info: ModelNewsDelete) -> list[dict] | list:
        """
        Delete Repository
        """
        try:
            async with self.session_factory() as session:
                if result := await session.scalars(
                    delete(News).where(News.article_id == news_info.article_id).returning(News)
                ):
                    news_list = result.all()
                    return [
                        {
                            "article_id": news.article_id,
                        }
                        for news in news_list
                    ]
                else:
                    return []
        except SQLAlchemyError as e:
            raise ex.InternalQuerryEx(ex=e)
