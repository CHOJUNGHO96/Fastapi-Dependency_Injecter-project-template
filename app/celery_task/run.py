import asyncio

from app.celery_task.container import Container as CeleryContainer

container = CeleryContainer()
celery_app = container.celery_app()


@celery_app.task
def run_news_crawling():
    news_crawling = container.celery_news_crawling()
    loop = asyncio.get_event_loop()
    if loop.is_running():
        # 현재 실행 중인 이벤트 루프가 있으면 새로운 태스크 생성
        loop.create_task(news_crawling.get_news_crawling_to_insert())
    else:
        # 실행 중인 이벤트 루프가 없으면 새 이벤트 루프 생성 및 실행
        new_loop = asyncio.new_event_loop()
        asyncio.set_event_loop(new_loop)
        new_loop.run_until_complete(news_crawling.get_news_crawling_to_insert())
        new_loop.close()
