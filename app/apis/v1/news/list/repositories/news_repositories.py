from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.news import News
from app.errors import exceptions as ex
from app.models.news import ModelNewsBase, ModelNewsRegister, ModelNewsUpdate


class NewsListRepository:
    """
    뉴스 리스트 Repository
    """

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_news_list_repository(self, news_info: ModelNewsBase) -> list[dict] | list:
        """
        Get Repository
        """
        try:
            async with self.session_factory() as session:
                conditions = []
                if news_info.article_id is not None:
                    conditions.append(News.article_id == news_info.article_id)
                if news_info.content is not None:
                    conditions.append(News.content == news_info.content)
                if news_info.source is not None:
                    conditions.append(News.source == news_info.source)
                if news_info.user_number is not None:
                    conditions.append(News.user_number == news_info.user_number)
                if news_info.url is not None:
                    conditions.append(News.url == news_info.url)
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
                        "user_number": news.user_number,
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

    async def put_news_list_repository(self, news_info: ModelNewsUpdate) -> list[dict] | list:
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
