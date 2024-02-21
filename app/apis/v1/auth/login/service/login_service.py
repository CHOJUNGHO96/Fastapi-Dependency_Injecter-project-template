from typing import Any

from fastapi.security import OAuth2PasswordRequestForm

from app.apis.v1.auth.authentication import Authentication
from app.apis.v1.auth.login.repositories.login_repositories import \
    LoginRepository
from app.database.redis_manger import init_redis_pool
from app.errors import exceptions as ex
from app.models.user import ModelTokenData


class LoginService:
    def __init__(
        self, login_repository: LoginRepository, config: dict, authentication: Authentication, redis: init_redis_pool
    ) -> None:
        self._repository: LoginRepository = login_repository
        self._config = config
        self.authentication = authentication
        self.redis = redis

    async def post_login_service(self, user_info: OAuth2PasswordRequestForm) -> ModelTokenData:
        """
        로그인 Service
        :param user_info: 유저정보
        """
        user_password = user_info.password
        del user_info.password

        # 레파지토리 호출
        response_user: dict[Any, Any] | None = await self._repository.post_login_repository(user_info)

        if response_user is None:
            raise ex.NotFoundUserEx()

        # 비밀번호 체크
        if self.authentication.verify_password(user_password, response_user["user_password"].encode("utf-8")):
            # JWT토큰 생성
            access_token = self.authentication.create_jwt_token(
                data={"sub": response_user["login_id"]}, conf=self._config, token_type="ACCESS"
            )
            refresh_token = self.authentication.create_jwt_token(
                data={"sub": response_user["login_id"]}, conf=self._config, token_type="REFRESH"
            )
            # 레디스에 유저정보 저장
            await self.redis.set(
                name=f"cahce_user_info_{response_user['login_id']}",
                value=str(
                    {
                        "user_id": response_user["user_id"],
                        "login_id": response_user["login_id"],
                        "user_name": response_user["user_name"],
                        "user_email": response_user["user_email"],
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    }
                ),
                ex=self._config.get("REDIS_EXPIRE_TIME", 604800),
            )
            return ModelTokenData(
                user_id=response_user["user_id"],
                login_id=response_user["login_id"],
                token_type="bearer",
                access_token=access_token,
                refresh_token=refresh_token,
            )
        else:
            raise ex.BadPassword()
