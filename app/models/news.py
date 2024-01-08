from pydantic import BaseModel


class NewsBase(BaseModel):
    article_id: int | None = None
    title: str | None = None
    content: str | None = None
    source: str | None = None
    url: str | None = None
    user_number: int | None = None
