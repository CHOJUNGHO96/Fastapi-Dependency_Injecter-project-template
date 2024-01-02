from sqlalchemy.orm import Session

from app.apis.v1.news.detail.repositories.news_repositories import \
    get_news_detail_repository


async def get_news_detail_service(session: Session, article_id: int):
    """
    뉴스 상세보기 Service
    :param session: DB 세션
    """

    # 레파지토리 호출
    news_list = await get_news_detail_repository(session, article_id)
    return news_list
