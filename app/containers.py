from celery import Celery
from dependency_injector import containers, providers
from fastapi.requests import Request

from app.apis.v1.auth.login.containers import Container as LoginContainer
from app.apis.v1.auth.registration.containers import \
    Container as RegistrationContainer
from app.apis.v1.news.list.containers import Container as NewsListContainer
from app.background.container import Container as BackgroundContainer
from app.common.config import get_config
from app.database.conn import Database
from app.database.redis_config import init_redis_pool
from app.util.logger import LogAdapter
from app.util.token import Token


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "app.database.redis_config",
        ],
    )

    # config 의존성 주입
    config = providers.Configuration()
    config.from_dict(get_config().dict())
    conf = config()

    # token 의존성 주입
    token = providers.Singleton(Token)

    # logging 의존성 주입
    logging = providers.Singleton(LogAdapter, request=Request, response=None, error=None)

    # db 의존성 주입
    db = providers.Singleton(Database, conf=config)

    # Redis 의존성 주입
    redis = providers.Resource(init_redis_pool, conf=config)

    # celery 인스턴스 의존성 주입
    celery_app = providers.Singleton(
        Celery,
        broker=f"redis://:{conf['REDIS_PASSWORD']}@{conf['REDIS_HOST']}:{conf['REDIS_PORT']}/0",
        imports=["background.base"],
    )

    # api 의존성 주입
    login_service = providers.Container(LoginContainer, db=db, config=config, token=token, redis=redis)
    registration_service = providers.Container(RegistrationContainer, db=db, config=config, token=token)
    news_list_service = providers.Container(NewsListContainer, db=db)

    # background 작업 의존성 주입
    celery_news_crawling = providers.Container(BackgroundContainer, db=db, celery_app=celery_app)
