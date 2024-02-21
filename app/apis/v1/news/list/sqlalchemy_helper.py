from app.database.schema.news import News
from app.models.news import ModelNewsBase


class SqlalchemyHelper:
    async def get_news_list_filter(self, news_schema: type[News], news_info: ModelNewsBase) -> list:
        """
        Filter
        """
        conditions = []
        if news_info.article_id is not None:
            conditions.append(news_schema.article_id == news_info.article_id)
        if news_info.user_id is not None:
            conditions.append(news_schema.user_id == news_info.user_id)
        if news_info.title is not None:
            conditions.append(news_schema.title.ilike(f"%{news_info.title}%"))
        if news_info.content is not None:
            conditions.append(news_schema.content.ilike(f"%{news_info.content}%"))
        if news_info.source is not None:
            conditions.append(news_schema.source.ilike(f"%{news_info.source}%"))
        if news_info.url is not None:
            conditions.append(news_schema.url.ilike(f"%{news_info.url}%"))

        return conditions
