from pydantic import BaseModel, EmailStr, Field


class ModelUserRegister(BaseModel):
    login_id: str = Field(example="로그인 아이디")
    user_password: str = Field(example="패스워드")
    user_email: EmailStr = Field(example="이메일")
    user_name: str = Field(example="이름")


class ModelTokenData(BaseModel):
    user_id: int | None = Field(default=None, example="유저번호")
    login_id: str | None = Field(default=None, example="로그인 아이디")
    access_token: str | None = Field(default=None, example="엑세스 토큰")
    refresh_token: str | None = Field(default=None, example="리프레시 토큰")
    token_type: str | None = Field(default=None, example="토큰타입")
