import asyncio

from app.celery_task.container import Container as CeleryContainer

container = CeleryContainer()
celery_app = container.celery_app()


@celery_app.task
def run_news_crawling():
    news_crawling = container.celery_news_crawling()
    asyncio.run(news_crawling.get_news_crawling_to_insert())
