from sqlalchemy import TIMESTAMP, Column, Date, Integer, String, Text
from sqlalchemy.sql import func

from app.database.base import BaseMixin
from app.database.schema.base import Base


class NewsArticle(Base, BaseMixin):
    __tablename__ = "news_articles"

    article_id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(100))
    published_date = Column(Date)
    scraped_date = Column(TIMESTAMP, default=func.current_timestamp())
    url = Column(String(255))
