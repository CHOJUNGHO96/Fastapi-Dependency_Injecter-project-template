import pandas as pd
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.errors import exceptions as ex
from app.util.init_template import QUERY_TEMPLATE
from app.util.jinja_sql import JINJA_SQL


async def get_news_list_repository(session: Session) -> list[dict]:
    """
    뉴스 리스트 Repository
    :param session: DB세션
    """
    try:
        query, bind_params = JINJA_SQL["pyformat"].prepare_query(
            QUERY_TEMPLATE["news.yaml"]["뉴스조회"],
            {},
        )
        news_info = pd.read_sql_query(sql=query, params=bind_params, con=session.connection()).to_dict("records")
        return news_info
    except SQLAlchemyError as e:
        raise ex.InternalQuerryEx(ex=e)
