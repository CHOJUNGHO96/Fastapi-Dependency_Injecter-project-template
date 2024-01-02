from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.conn import Database as db
from app.models.news import NewsBase

from .service.news_service import get_news_list_service

router = APIRouter()


@router.get("/list", response_model=NewsBase)
async def get_news_list_resources(
    session: Session = Depends(db.session),
):
    """
    `뉴스 리스트 조회`\n
    :param session: DB 세션\n
    """
    response = await get_news_list_service(session)
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(status_code=404, content={"message": "news Not Found", "code": "404"})
    )
