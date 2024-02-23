from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.apis.v1.auth.registration.containers import Container
from app.apis.v1.auth.registration.service.registration_service import (
    RegistrationService,
)
from app.models.response import ResponseModel
from app.models.user import ModelUserRegister

router = APIRouter()


@router.post("/register", response_model=ResponseModel)
@inject
async def post_registration(
    user_info: ModelUserRegister,
    registration_service: RegistrationService = Depends(Provide[Container.registration_service]),
):
    """
    `회원가입 API`
    """
    if await registration_service.post_register_service(user_info):
        return JSONResponse(content={"status": 200, "msg": "Success Register.", "code": 200, "list": []})
    else:
        return JSONResponse(
            status_code=422, content={"status": 422, "msg": "Fail to register", "code": 422, "list": []}
        )
