from sqlalchemy import Column, Integer, String, Text, DateTime

from .base import Base


class News(Base):
    __tablename__ = "news_articles"

    article_id = Column(Integer, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    source = Column(String(100), nullable=False)
    reg_date = Column(DateTime)
    url = Column(String(255), nullable=False)
    user_number = Column(Integer, nullable=False)
    is_enable = Column(Integer, default=1)
