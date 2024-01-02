from pydantic import BaseModel


class UserBase(BaseModel):
    user_id: str
    user_password: str
    user_email: str | None = None
    user_name: str | None = None


class UserRegister(UserBase):
    user_email: str
    user_name: str


class UserInDB(UserBase):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    user_id: str | None = None
