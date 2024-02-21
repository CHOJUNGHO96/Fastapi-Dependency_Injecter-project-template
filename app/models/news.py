from pydantic import BaseModel


class ModelNewsBase(BaseModel):
    article_id: int | None = None
    title: str | None = None
    content: str | None = None
    source: str | None = None
    url: str | None = None
    user_id: int | None = None


class ModelNewsRegister(BaseModel):
    title: str
    content: str
    source: str
    url: str
    user_id: int


class ModelNewsPut(ModelNewsBase):
    article_id: int


class ModelNewsDelete(BaseModel):
    article_id: int
