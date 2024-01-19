from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.background.worker import celery_app

router = APIRouter()


@router.get("/news_crawling")
async def get_news_list_resources():
    """
    `뉴스 크롤링 백그라운드 실행`
    """
    celery_app.send_task("background.run.run_news_crawling")
    return JSONResponse(content={"message": "background run success", "list": []})
