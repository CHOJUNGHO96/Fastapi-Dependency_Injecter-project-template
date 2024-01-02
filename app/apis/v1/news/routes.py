from fastapi import APIRouter

import app.apis.v1.news.detail.end_point as news_detail
import app.apis.v1.news.list.end_point as news_list

news_api_router = APIRouter()
news_api_router.include_router(news_list.router, tags=["News"])
news_api_router.include_router(news_detail.router, tags=["News"])
