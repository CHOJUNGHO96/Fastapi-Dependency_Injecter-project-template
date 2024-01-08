from fastapi import APIRouter, Depends
from fastapi.security import APIKeyHeader

from app.apis.v1.auth.routes import auth_api_router
from app.apis.v1.news.routes import news_api_router

API_KEY_HEADER = APIKeyHeader(name="Authorization", auto_error=False)
api_router = APIRouter()
api_router.include_router(auth_api_router, prefix="/auth")
api_router.include_router(news_api_router, prefix="/news", dependencies=[Depends(API_KEY_HEADER)])
