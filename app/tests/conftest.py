import asyncio
import os
from typing import Generator

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient


@pytest.fixture(scope="session")
def app() -> FastAPI:
    """
    테스트용 app
    """
    os.environ["API_MODE"] = "test"

    from app.main import create_app

    yield create_app()


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop, None, None]:
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session")
def client(app: FastAPI):
    """
    테스트용 클라이언트
    """
    with TestClient(app, base_url="http://127.0.0.1/api/v1") as client:
        yield client
