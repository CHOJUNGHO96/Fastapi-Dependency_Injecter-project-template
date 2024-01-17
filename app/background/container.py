from celery import Celery
from dependency_injector import containers, providers

from app.background.job.news_crawling import NewsCrawling
from app.common.config import get_config
from app.database.conn import Database


class Container(containers.DeclarativeContainer):
    # config 의존성 주입
    config = providers.Configuration()
    config.from_dict(get_config().dict())
    conf = config()

    # db 인스턴스 의존성 주입
    db = providers.Singleton(Database, conf=config)

    # celery 인스턴스 의존성 주입
    celery_app = providers.Singleton(
        Celery,
        broker=f"redis://:{conf['REDIS_PASSWORD']}@{conf['REDIS_HOST']}:{conf['REDIS_PORT']}/0",
        imports=["background.run"],
    )

    # news_crawling
    celery_news_crawling = providers.Singleton(NewsCrawling, session_factory=db.provided.session)
