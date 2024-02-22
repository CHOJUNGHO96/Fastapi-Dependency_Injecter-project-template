import app.apis.v1.news.list.end_point as news_list
from fastapi import APIRouter

news_api_router = APIRouter()
news_api_router.include_router(news_list.router, tags=["News"])
