from fastapi import APIRouter
from fastapi.responses import JSONResponse

router = APIRouter()


@router.post("/logout")
async def post_logout():
    """
    `로그아웃  API`
    """
    response = JSONResponse(content={"message": "Suceess Logout."})
    response.delete_cookie(key="token_type")
    response.delete_cookie(key="access_token")
    return response
