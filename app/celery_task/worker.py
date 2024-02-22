from app.celery_task.container import Container
from celery import Celery
from celery.schedules import crontab
from dependency_injector import containers

container: containers = Container()
celery_app: Celery = container.celery_app()

# 타임존 초기화
celery_app.conf.timezone = "Asia/Seoul"

# beat 스케줄 초기화
celery_app.conf.beat_schedule = {
    "run_news_crawling_1_min": {
        "task": "app.celery_task.run.run_news_crawling",
        # "schedule": 20.0,
        "schedule": crontab(hour="7", minute="0"),
    },
}
