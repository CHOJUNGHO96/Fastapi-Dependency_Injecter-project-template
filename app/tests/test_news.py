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


@pytest.mark.asyncio
async def test_get_news_list(client: TestClient):
    response = client.get(
        url="news/list",
    )
    assert response.status_code == 200
