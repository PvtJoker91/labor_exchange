import pytest
import pytest_asyncio
from fastapi import FastAPI
from fastapi.testclient import TestClient
from dishka.integrations.fastapi import setup_dishka
from dishka import make_async_container

from core.config import Settings, settings
from main import create_app
from tests.fixtures import MockSessionProvider


@pytest.fixture
def app() -> FastAPI:
    app = create_app()
    return app


@pytest_asyncio.fixture
async def container():
    container = make_async_container(MockSessionProvider(), context={Settings: settings})
    yield container
    await container.close()


@pytest.fixture
def client(app, container):
    setup_dishka(container, app)
    with TestClient(app) as client:
        yield client
