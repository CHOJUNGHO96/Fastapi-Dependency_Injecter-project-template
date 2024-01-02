from dataclasses import asdict

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

from app.apis.v1.bridge_routes import api_router
from app.common.config import get_config
from app.containers import Container
from app.middlewares.base_middleware import base_control_middlewares


def create_app() -> FastAPI:
    """
    FastApi 앱 실행
    """
    # 컨테이너 초기화
    container = Container()

    _app = FastAPI()

    _app.container = container

    conf = get_config()

    # 미들웨어 정의
    _app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=base_control_middlewares)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=conf.ALLOW_SITE,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터정의
    _app.include_router(api_router, prefix="/api/v1")

    return _app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="192.168.164.1", port=5050, reload=True)
