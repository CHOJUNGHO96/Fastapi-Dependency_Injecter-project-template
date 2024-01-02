from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from app.apis.v1.auth.login.containers import Container
from app.models.user import Token, UserBase

from .service.login_service import LoginService

router = APIRouter()


@router.post("/login", response_model=Token)
@inject
async def post_login(
    user_info: UserBase,
    login_service: LoginService = Depends(Provide[Container.login_service]),
):
    """
    `로그인 API`\n
    :param user_info: 유저정보\n
    """
    return await login_service.post_login_service(user_info)
