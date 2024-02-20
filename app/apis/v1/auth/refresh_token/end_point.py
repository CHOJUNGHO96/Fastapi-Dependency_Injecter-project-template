from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, Response, requests

from app.apis.v1.auth.refresh_token.containers import Container
from app.apis.v1.auth.refresh_token.service.refresh_token_service import \
    RefreshTokenService
from app.models.user import ModelTokenData

router = APIRouter()


@router.get("/refresh_token")
@inject
async def get_refresh_token(
    req: requests.Request,
    response: Response,
    user_id: str,
    refresh_token_service: RefreshTokenService = Depends(Provide[Container.refresh_token_service]),
):
    """
    `토큰재발급 API`
    """
    if "refresh_token" in req.cookies:
        user_data: ModelTokenData = await refresh_token_service.get_refresh_token_service(user_id)
        response.set_cookie(
            key="token_type",
            value=user_data.token_type,
        )
        response.set_cookie(key="access_token", value=user_data.access_token)
        response.set_cookie(key="refresh_token", value=user_data.refresh_token)
        return user_data
    else:
        return {"status_code": 401, "message": "refresh_token not in cookies"}
