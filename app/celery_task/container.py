from app.celery_task.job.news_crawling import NewsCrawling
from app.common.config import get_config
from app.database.conn import Database
from celery import Celery
from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    # config 의존성 주입
    config = providers.Configuration()
    config.from_dict(get_config().dict())
    conf = config()

    # db 인스턴스 의존성 주입
    db = providers.Factory(Database, conf=config)

    # celery 인스턴스 의존성 주입
    celery_app = providers.Factory(
        Celery,
        broker=f"redis://:{conf['REDIS_PASSWORD']}@{conf['REDIS_HOST']}:{conf['REDIS_PORT']}/0",
        imports=["app.celery_task.run"],
    )

    # news_crawling
    celery_news_crawling = providers.Factory(NewsCrawling, session_factory=db.provided.session)
