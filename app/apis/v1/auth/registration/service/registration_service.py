import bcrypt

from app.apis.v1.auth.authentication import Authentication
from app.apis.v1.auth.registration.repositories.registration_repositories import (
    RegistrationRepository,
)
from app.models.user import ModelUserRegister


class RegistrationService:
    def __init__(
        self, Registration_repository: RegistrationRepository, config: dict, authentication: Authentication
    ) -> None:
        self._repository: RegistrationRepository = Registration_repository
        self._config = config
        self.authentication = authentication

    async def post_register_service(self, user_info: ModelUserRegister) -> bool:
        """
        회원가입 Service
        :param user_info: 유저정보
        """

        # 아이디, 이메일 중복체크
        await self._repository.check_user(user_info)

        # 비밀번호 해쉬화
        hashed_password = bcrypt.hashpw(user_info.user_password.encode("utf-8"), bcrypt.gensalt())

        # 암호화된 비밀번호를 DB에 넣기위해 디코딩하여 다시 p["password"]에 저장
        user_info.user_password = hashed_password.decode("utf-8")

        return await self._repository.post_register_repository(user_info)
