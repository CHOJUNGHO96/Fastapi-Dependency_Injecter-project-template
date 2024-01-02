from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.apis.v1.auth.registration.containers import Container
from app.apis.v1.auth.registration.service.registration_service import \
    RegistrationService
from app.models.user import Token, UserRegister

router = APIRouter()


@router.post("/register", response_model=Token)
@inject
async def post_registration(
    user_info: UserRegister,
    registration_service: RegistrationService = Depends(Provide[Container.registration_service]),
):
    """
    `회원가입 API`\n
    :param user_info: 유저정보\n
    """
    return await registration_service.post_register_service(user_info)
