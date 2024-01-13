"""Tests module."""
import pytest
from fastapi.testclient import TestClient


@pytest.mark.asyncio
async def test_get_news_list(client: TestClient):
    response = client.get(
        url="news/list",
    )
    assert response.status_code == 200
