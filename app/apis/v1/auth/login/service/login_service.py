from typing import Any

import bcrypt
from fastapi.responses import JSONResponse

from app.apis.v1.auth.login.repositories.login_repositories import \
    LoginRepository
from app.database.redis_config import init_redis_pool
from app.models.user import ModelTokenData, ModelUserBase
from app.util.token import Token


class LoginService:
    def __init__(self, login_repository: LoginRepository, config: dict, token: Token, redis: init_redis_pool) -> None:
        self._repository: LoginRepository = login_repository
        self._config = config
        self._token = token
        self.redis = redis

    async def post_login_service(self, user_info: ModelUserBase) -> ModelTokenData | JSONResponse:
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

        if bcrypt.checkpw(password.encode(), response_user["user_password"].encode("utf-8")):
            # JWT토큰 생성
            access_token = self._token.create_access_token(data={"sub": response_user["user_id"]}, conf=self._config)
            # 레디스에 유저정보 저장
            await self.redis.set(
                name=f"cahce_user_info_{response_user['user_id']}",
                value=str(
                    {
                        "user_number": response_user["user_number"],
                        "user_id": response_user["user_id"],
                        "user_name": response_user["user_name"],
                        "user_email": response_user["user_email"],
                        "access_token": access_token,
                    }
                ),
                ex=self._config.get("REDIS_EXPIRE_TIME", 86400),
            )
            return ModelTokenData(user_id=response_user["user_id"], token_type="bearer", access_token=access_token)
        else:
            return JSONResponse(status_code=400, content=dict(msg="비밀번호가 일치하지 않습니다.", code="400"))
