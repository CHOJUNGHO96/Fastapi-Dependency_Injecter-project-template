from pydantic import BaseModel, Field


class ModelNewsBase(BaseModel):
    article_id: int | None = Field(default=None, example="뉴스기사 번호")
    title: str | None = Field(default=None, example="뉴스기사 제목")
    content: str | None = Field(default=None, example="뉴스기사 내용")
    source: str | None = Field(default=None, example="뉴스기사 출처")
    url: str | None = Field(default=None, example="뉴스기사 URL")
    user_id: int | None = Field(default=None, example="작성자")


class ModelNewsRegister(BaseModel):
    title: str = Field(default=None, example="뉴스기사 제목")
    content: str = Field(default=None, example="뉴스기사 내용")
    source: str = Field(default=None, example="뉴스기사 출처")
    url: str = Field(default=None, example="뉴스기사 URL")
    user_id: int = Field(default=None, example="작성자")


class ModelNewsPut(ModelNewsBase):
    article_id: int = Field(default=None, example="뉴스기사 번호")


class ModelNewsDelete(BaseModel):
    article_id: int = Field(default=None, example="뉴스기사 번호")
