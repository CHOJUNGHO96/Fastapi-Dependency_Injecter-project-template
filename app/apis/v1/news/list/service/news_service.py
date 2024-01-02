from sqlalchemy.orm import Session

from app.apis.v1.news.list.repositories.news_repositories import \
    get_news_list_repository


async def get_news_list_service(session: Session):
    """
    뉴스 리스트  Service
    :param session: DB 세션
    """

    # 레파지토리 호출
    news_list = await get_news_list_repository(session)
    return news_list
