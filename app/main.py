import uvicorn
from app.apis.v1.bridge_routes import api_router
from app.containers import Container
from app.middlewares.dispatch import dispatch_middleware
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from starlette.middleware.base import BaseHTTPMiddleware


def create_app() -> FastAPI:
    """
    FastApi 앱 실행
    """
    # 컨테이너 초기화
    container = Container()

    _app = FastAPI()

    _app.container = container

    # 미들웨어 정의
    _app.add_middleware(middleware_class=BaseHTTPMiddleware, dispatch=dispatch_middleware)

    _app.add_middleware(
        CORSMiddleware,
        allow_origins=_app.container.config()["ALLOW_SITE"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # 라우터정의
    _app.include_router(api_router, prefix="/api/v1")

    # API 문서 정의
    def custom_openapi():
        if app.openapi_schema:
            return app.openapi_schema
        openapi_schema = get_openapi(
            title=_app.container.config()["PROJECT_NAME"],
            version=_app.container.config()["VERSION"],
            summary="A project that can serve as a base for productivity when developing a backend web server with fastApi",
            routes=_app.routes,
        )
        app.openapi_schema = openapi_schema
        return app.openapi_schema

    _app.openapi = custom_openapi
    return _app


app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", port=5050, reload=True)
