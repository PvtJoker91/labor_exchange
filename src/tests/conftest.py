import pytest_asyncio

from dishka import make_async_container

from core.config import Settings, settings
from tests.fixtures import MockProvider


@pytest_asyncio.fixture
async def mock_container():
    container = make_async_container(MockProvider(), context={Settings: settings})
    yield container
    await container.close()
