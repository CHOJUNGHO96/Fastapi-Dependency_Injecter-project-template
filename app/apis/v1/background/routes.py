import app.apis.v1.background.news_crawling.end_point as news_crawling
from fastapi import APIRouter

background_api_router = APIRouter()
background_api_router.include_router(news_crawling.router, tags=["background"])
