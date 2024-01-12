from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.apis.v1.news.list.containers import Container
from app.models.news import (ModelNewsBase, ModelNewsRegister,
                             ModelNewsRegisterResponse)

from .service.news_service import NewsListService

router = APIRouter()


@router.get("/list", response_model=ModelNewsBase)
@inject
async def get_news_list_resources(
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 조회`\n
    """
    response = await news_list_service.get_news_list_service()
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(content={"message": "news Not Found", "list": response})
    )


@router.post("/list", response_model=ModelNewsRegisterResponse)
@inject
async def post_news_list_resources(
    news_info: ModelNewsRegister,
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 등록`\n
    """
    response = await news_list_service.post_news_list_service(news_info)
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(status_code=404, content={"message": "Registration failed."})
    )
