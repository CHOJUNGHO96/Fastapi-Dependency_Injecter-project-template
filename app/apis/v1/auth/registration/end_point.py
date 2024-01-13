from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.apis.v1.auth.registration.containers import Container
from app.apis.v1.auth.registration.service.registration_service import \
    RegistrationService
from app.models.user import ModelToken, ModelUserRegister

router = APIRouter()


@router.post("/register", response_model=ModelToken)
@inject
async def post_registration(
    user_info: ModelUserRegister,
    registration_service: RegistrationService = Depends(Provide[Container.registration_service]),
):
    """
    `회원가입 API`
    """
    return await registration_service.post_register_service(user_info)
