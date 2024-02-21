from typing import Any

from app.apis.v1.auth.authentication import Authentication
from app.apis.v1.auth.refresh_token.repositories.refresh_token_repositories import \
    RefreshTokenRepository
from app.database.redis_manger import init_redis_pool
from app.errors import exceptions as ex
from app.models.user import ModelTokenData


class RefreshTokenService:
    def __init__(
        self,
        refresh_token_repository: RefreshTokenRepository,
        config: dict,
        authentication: Authentication,
        redis: init_redis_pool,
    ) -> None:
        self._repository: RefreshTokenRepository = refresh_token_repository
        self._config = config
        self.authentication = authentication
        self.redis = redis

    async def get_refresh_token_service(self, user_id: str) -> ModelTokenData:
        """
        Refresh Token Service
        """
        # 레파지토리 호출
        response_user: dict[Any, Any] | None = await self._repository.get_refresh_token_repository(user_id)

        if response_user is None:
            raise ex.NotFoundUserEx()

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
