from app.apis.v1.auth.login.containers import Container
from app.models.response import ResponseModel
from app.models.user import ModelTokenData
from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm

from .service.login_service import LoginService

router = APIRouter()


@router.post("/login", response_model=ResponseModel)
@inject
async def post_login(
    user_info: OAuth2PasswordRequestForm = Depends(),
    login_service: LoginService = Depends(Provide[Container.login_service]),
):
    """
    `로그인 API`
    """
    user_data: ModelTokenData = await login_service.post_login_service(user_info)
    if user_data:
        response = JSONResponse(content={"status": 200, "msg": "Success Login.", "code": 200, "list": user_data.dict()})
        response.set_cookie("token_type", user_data.token_type)
        response.set_cookie("access_token", user_data.access_token)
        response.set_cookie("refresh_token", user_data.refresh_token)
        return response
    else:
        return JSONResponse(status_code=422, content={"status": 422, "msg": "Fail to login", "code": 422, "list": []})
