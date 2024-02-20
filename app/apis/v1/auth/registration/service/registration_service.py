import bcrypt

from app.apis.v1.auth.registration.repositories.registration_repositories import \
    RegistrationRepository
from app.models.user import ModelTokenData, ModelUserRegister
from app.util.token import Token


class RegistrationService:
    def __init__(self, Registration_repository: RegistrationRepository, config: dict, token: Token) -> None:
        self._repository: RegistrationRepository = Registration_repository
        self._config = config
        self._token = token

    async def post_register_service(self, user_info: ModelUserRegister) -> ModelTokenData:
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

        # 레파지토리 호출
        user_info: dict | None = await self._repository.post_register_repository(user_info)

        # JWT토큰 생성
        access_token = self._token.create_access_token(data={"sub": user_info["user_id"]}, conf=self._config)

        return ModelTokenData(user_id=user_info["user_id"], token_type="bearer", access_token=access_token)
