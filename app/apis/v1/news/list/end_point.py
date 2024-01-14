from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.apis.v1.news.list.containers import Container
from app.models.news import (ModelNewsBase, ModelNewsCudResponse,
                             ModelNewsDelete, ModelNewsPut, ModelNewsRegister)

from .service.news_service import NewsListService

router = APIRouter()


@router.get("/list", response_model=ModelNewsBase)
@inject
async def get_news_list_resources(
    new_info: ModelNewsBase = Depends(ModelNewsBase),
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 조회`
    """
    response = await news_list_service.get_news_list_service(new_info)
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(content={"message": "News Not Found", "list": response})
    )


@router.post("/list", response_model=ModelNewsCudResponse)
@inject
async def post_news_list_resources(
    news_info: ModelNewsRegister,
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 등록`
    """
    response = await news_list_service.post_news_list_service(news_info)
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(status_code=404, content={"message": "Registration Failed."})
    )


@router.put("/list", response_model=ModelNewsCudResponse)
@inject
async def put_news_list_resources(
    news_info: ModelNewsPut,
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 수정`
    """
    response = await news_list_service.put_news_list_service(news_info)
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(status_code=404, content={"message": "Update Failed."})
    )


@router.delete("/list", response_model=ModelNewsCudResponse)
@inject
async def delete_news_list_resources(
    news_info: ModelNewsDelete = Depends(ModelNewsDelete),
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 삭제`
    """
    response = await news_list_service.delete_news_list_service(news_info)
    return (
        JSONResponse(content={"list": response})
        if response
        else JSONResponse(status_code=404, content={"message": "Delete Failed."})
    )
