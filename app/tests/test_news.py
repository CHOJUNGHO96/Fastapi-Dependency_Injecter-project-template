"""Tests module."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_post_news_list(client: TestClient):
    response = client.post(
        url="news/list",
        json={
            "title": "test_title",
            "content": "test_content",
            "source": "test_source",
            "url": "test_url",
            "user_number": client.app_state["user_number"],
        },
    )
    assert response.status_code == 200
    response_body = response.json()
    client.app_state.update({"article_id": response_body["list"][0]["article_id"]})


@pytest.mark.asyncio
async def test_put_news_list(client: TestClient):
    response = client.put(
        url="news/list",
        json={
            "title": "test_title2",
            "article_id": client.app_state["article_id"],
        },
    )
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_get_news_list(client: TestClient):
    response = client.get(
        url="news/list",
        params={"title": "test_title2", "article_id": client.app_state["article_id"]},
    )
    response_body = response.json()
    assert response.status_code == 200
    assert response_body["list"][0]["article_id"] == client.app_state["article_id"]


@pytest.mark.asyncio
async def test_delete_news_list(client: TestClient):
    response = client.delete(
        url="news/list",
        params={"article_id": client.app_state["article_id"]},
    )
    assert response.status_code == 200
