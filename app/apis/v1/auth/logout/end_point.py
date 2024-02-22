from app.models.response import ResponseModel
from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/logout", response_model=ResponseModel)
async def post_logout():
    """
    `로그아웃  API`
    """
    response = JSONResponse(content={"status": 200, "msg": "Suceess Logout.", "code": 200, "list": []})
    response.delete_cookie(key="token_type")
    response.delete_cookie(key="access_token")
    response.delete_cookie(key="refresh_token")
    return response
