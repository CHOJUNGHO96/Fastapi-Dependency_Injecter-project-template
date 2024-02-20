from pydantic import BaseModel


class ModelUserBase(BaseModel):
    user_id: str
    user_password: str
    user_email: str | None = None
    user_name: str | None = None


class ModelUserRegister(ModelUserBase):
    user_email: str
    user_name: str


class ModelUserInDB(ModelUserBase):
    hashed_password: str


class ModelTokenData(BaseModel):
    user_id: str | None = None
    access_token: str | None = None
    token_type: str | None = None
