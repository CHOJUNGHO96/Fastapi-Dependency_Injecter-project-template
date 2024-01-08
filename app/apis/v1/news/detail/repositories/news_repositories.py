import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.errors import exceptions as ex


async def get_news_detail_repository(session: Session, article_id: int) -> list[dict]:
    """
    뉴스 상세보기 Repository
    :param session: DB세션
    """
    ...
    # try:
    #     query, bind_params = JINJA_SQL["pyformat"].prepare_query(
    #         QUERY_TEMPLATE["news.yaml"]["뉴스조회"],
    #         {"article_id": article_id},
    #     )
    #     news_info = pd.read_sql_query(sql=query, params=bind_params, con=session.connection()).to_dict("records")
    #     return news_info
    # except SQLAlchemyError as e:
    #     raise ex.InternalQuerryEx(ex=e)
