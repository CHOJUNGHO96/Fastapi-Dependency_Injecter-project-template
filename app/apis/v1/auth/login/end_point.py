from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response

from app.apis.v1.auth.login.containers import Container
from app.models.user import ModelTokenData, ModelUserBase

from .service.login_service import LoginService

router = APIRouter()


@router.post("/login", response_model=ModelTokenData)
@inject
async def post_login(
    user_info: ModelUserBase,
    response: Response,
    login_service: LoginService = Depends(Provide[Container.login_service]),
):
    """
    `로그인 API`
    """
    user_data = await login_service.post_login_service(user_info)
    response.set_cookie("token_type", user_data.token_type)
    response.set_cookie("access_token", user_data.access_token)
    response.set_cookie("refresh_token", user_data.refresh_token)
    return user_data
