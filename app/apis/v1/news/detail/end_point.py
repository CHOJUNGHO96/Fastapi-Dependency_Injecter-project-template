from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.database.conn import Database as db
from app.models.news import ModelNewsBase

from .service.news_service import get_news_detail_service

router = APIRouter()


@router.get("/detail", response_model=ModelNewsBase)
async def get_news_detail_resources(
    article_id: int,
    session: Session = Depends(db.session),
):
    """
    `뉴스 상세보기 조회`\n
    :article_id: 뉴스 아이디\n
    :param session: DB 세션\n
    """
    response = await get_news_detail_service(session, article_id)
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(status_code=404, content={"message": "news Not Found", "code": "404"})
    )
