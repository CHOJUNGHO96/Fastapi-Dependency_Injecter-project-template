from app.apis.v1.news.list.repositories.news_repositories import \
    NewsListRepository


class NewsListService:
    def __init__(self, news_list_repository: NewsListRepository) -> None:
        self._repository: NewsListRepository = news_list_repository

    async def get_news_list_service(self) -> list[dict] | list:
        """
        뉴스 리스트  Service
        """

        # 레파지토리 호출
        news_list: list[dict] = await self._repository.get_news_list_repository()
        return news_list
