from contextlib import AbstractAsyncContextManager
from typing import Callable

from sqlalchemy import insert, select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.news import News
from app.errors import exceptions as ex
from app.models.news import ModelNewsRegister


class NewsListRepository:
    """
    뉴스 리스트 Repository
    """

    def __init__(self, session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]]) -> None:
        self.session_factory = session_factory

    async def get_news_list_repository(self) -> list[dict] | list:
        """
        Get Repository
        """
        try:
            async with self.session_factory() as session:
                result = await session.scalars(select(News))
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
