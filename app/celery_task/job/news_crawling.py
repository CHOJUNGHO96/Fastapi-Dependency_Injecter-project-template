from contextlib import AbstractAsyncContextManager
from typing import Callable

from bs4 import BeautifulSoup
from selenium import webdriver
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.schema.news import News


class NewsCrawling:
    """
    뉴스 크롤링
    """

    def __init__(
        self,
        session_factory: Callable[..., AbstractAsyncContextManager[AsyncSession]],
    ) -> None:
        self.session_factory = session_factory

    async def get_news_crawling_to_insert(self) -> list[dict] | list:
        """
        뉴스 크롤링해와서 DB에 INSERT 해주는 함수
        """

        async with self.session_factory() as session:
            get_last_news = await session.scalars(select(News).order_by(News.article_id.desc()).limit(1))
            if news_data := get_last_news.first():
                url_id = int(news_data.url.split("=")[-1])
            else:
                url_id = 264834

        # selenium 설정
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")

        insert_target = []
        for _url_id in range(url_id + 1, url_id + 4):
            try:
                driver = webdriver.Chrome(options=chrome_options)

                # 크롤링할 페이지 접속
                url = f"https://www.arirang.com/news/view/?id={str(_url_id)}"
                driver.get(url)

                # 페이지의 소스 가져오기
                html = driver.page_source
                soup = BeautifulSoup(html, "html.parser")

                # title 추출
                title = soup.find("div", class_="title").get_text(strip=True)

                # content 추출
                content_paragraphs = soup.find_all("p", class_="text")
                content = " ".join(p.get_text(strip=True) for p in content_paragraphs)

                # 브라우저 닫기
                driver.quit()
                insert_target.append({"title": title, "content": content, "url": url, "source": "아리랑TV", "user_id": 1})
            except Exception as e:
                print(e)
                continue

        async with self.session_factory() as session:
            if result := await session.execute(insert(News).values(insert_target).returning(News)):
                news_list = result.all()
                return [
                    {
                        "article_id": news[0].article_id,
                    }
                    for news in news_list
                ]
            else:
                return []
