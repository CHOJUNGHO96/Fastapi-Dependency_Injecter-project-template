from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.celery_task.worker import celery_app
from app.models.response import ResponseModel

router = APIRouter()


@router.get("/news_crawling", response_model=ResponseModel)
async def get_news_list_resources():
    """
    `뉴스 크롤링 백그라운드 실행`
    """
    celery_app.send_task("background.run.run_news_crawling")
    return JSONResponse(content={"status": 200, "msg": "Success News Crawling.", "code": "200", "list": []})
