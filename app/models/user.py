from pydantic import BaseModel


class ModelUserRegister(BaseModel):
    login_id: str
    user_password: str
    user_email: str
    user_name: str


class ModelTokenData(BaseModel):
    user_id: int | None = None
    login_id: str | None = None
    access_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
