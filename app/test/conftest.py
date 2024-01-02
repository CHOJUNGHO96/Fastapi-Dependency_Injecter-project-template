import os

import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.database.conn import db
from app.main import create_app


@pytest.fixture(scope="session")
def app():
    """
    테스트용 app
    :return:
    """
    os.environ["CJH_API_MODE"] = "test"
    return create_app()


@pytest.fixture(scope="session")
def client(app):
    """
    테스트용 클라이언트
    :param app:
    :return:
    """
    return AsyncClient(app=app, base_url="http://127.0.0.1:8080")


@pytest.fixture(scope="function", autouse=True)
def session():
    """
    db session
    :return:
    """
    db_session = next(db.session())
    yield session
    db_session.rollback()


@pytest.fixture(scope="function")
def delete_data():
    """
    테스트전 모든 테이블 데이터 삭제
    :return:
    """
    db_session = next(db.session())

    table = db_session.execute(
        text(
            """
SELECT tablename
FROM pg_catalog.pg_tables
WHERE schemaname != 'pg_catalog'
    AND schemaname != 'information_schema'
    AND tablename != 'global_config';      
        """
        )
    ).fetchall()

    try:
        for t in table:
            query = f"TRUNCATE {t[0]}; "
            db_session.execute(text(query))
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        raise e
