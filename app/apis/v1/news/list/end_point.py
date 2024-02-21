from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from app.apis.v1.news.list.containers import Container
from app.models.news import (ModelNewsBase, ModelNewsDelete, ModelNewsPut,
                             ModelNewsRegister)
from app.models.response import ResponseModel

from .service.news_service import NewsListService

router = APIRouter()


@router.get("/list", response_model=ResponseModel)
@inject
async def get_news_list_resources(
    news_info: ModelNewsBase = Depends(ModelNewsBase),
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 조회`
    """
    news_list: list = await news_list_service.get_news_list_service(news_info)
    if news_list:
        return JSONResponse(content={"status": 200, "msg": "Success Get News List.", "code": "200", "list": news_list})
    else:
        return JSONResponse(
            status_code=422, content={"status": 422, "msg": "News Not Found", "code": "422", "list": []}
        )


@router.post("/list", response_model=ResponseModel)
@inject
async def post_news_list_resources(
    news_info: ModelNewsRegister,
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 등록`
    """
    news_list: list = await news_list_service.post_news_list_service(news_info)
    if news_list:
        return JSONResponse(
            content={"status": 200, "msg": "Success Registrate News List.", "code": "200", "list": news_list}
        )
    else:
        return JSONResponse(
            status_code=422, content={"status": 422, "msg": "Fail to news registrate", "code": "422", "list": []}
        )


@router.put("/list", response_model=ResponseModel)
@inject
async def put_news_list_resources(
    news_info: ModelNewsPut,
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 수정`
    """
    news_list: list = await news_list_service.put_news_list_service(news_info)
    if news_list:
        return JSONResponse(
            content={"status": 200, "msg": "Success Update News List.", "code": "200", "list": news_list}
        )
    else:
        return JSONResponse(
            status_code=422, content={"status": 422, "msg": "Fail to news update", "code": "422", "list": []}
        )


@router.delete("/list", response_model=ResponseModel)
@inject
async def delete_news_list_resources(
    news_info: ModelNewsDelete = Depends(ModelNewsDelete),
    news_list_service: NewsListService = Depends(Provide[Container.news_list_service]),
):
    """
    `뉴스 리스트 삭제`
    """
    news_list: list = await news_list_service.delete_news_list_service(news_info)
    if news_list:
        return JSONResponse(
            content={"status": 200, "msg": "Success Delte News List.", "code": "200", "list": news_list}
        )
    else:
        return JSONResponse(
            status_code=422, content={"status": 422, "msg": "Fail to news delete", "code": "422", "list": []}
        )
