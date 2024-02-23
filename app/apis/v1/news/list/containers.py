from dependency_injector import containers, providers

from app.apis.v1.news.list.repositories.news_repositories import NewsListRepository
from app.apis.v1.news.list.service.news_service import NewsListService
from app.apis.v1.news.list.sqlalchemy_helper import SqlalchemyHelper


class Container(containers.DeclarativeContainer):
    db = providers.Singleton()

    sqlalchemy_helper = providers.Singleton(SqlalchemyHelper)

    wiring_config = containers.WiringConfiguration(packages=["app.apis.v1.news.list"])

    # Repository
    news_list_repository = providers.Factory(
        NewsListRepository, session_factory=db.provided.session, sqlalchemy_helper=sqlalchemy_helper
    )

    # Service
    news_list_service = providers.Factory(NewsListService, news_list_repository=news_list_repository)
