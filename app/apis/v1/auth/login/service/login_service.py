from typing import Any

import bcrypt
from fastapi.responses import JSONResponse

from app.apis.v1.auth.login.repositories.login_repositories import \
    LoginRepository
from app.models.user import UserBase
from app.util.token import Token


class LoginService:
    def __init__(self, login_repository: LoginRepository, config: dict, token: Token) -> None:
        self._repository: LoginRepository = login_repository
        self._config = config
        self._token = token

    async def post_login_service(self, user_info: UserBase):
        """
        로그인 Service
        :param user_info: 유저정보
        """
        password = user_info.user_password
        del user_info.user_password

        # 레파지토리 호출
        response_user: dict[Any, Any] | None = await self._repository.post_login_repository(user_info)

        if response_user is None:
            return JSONResponse(status_code=400, content=dict(msg="아이디가 존재하지 않습니다.", code="400"))

        if bcrypt.checkpw(password.encode("utf-8"), response_user["user_password"].encode("utf-8")):
            # JWT토큰 생성
            access_token = self._token.create_access_token(data={"sub": response_user["user_id"]}, conf=self._config)
            return {"access_token": access_token, "token_type": "bearer"}
        else:
            return JSONResponse(status_code=400, content=dict(msg="비밀번호가 일치하지 않습니다.", code="400"))
