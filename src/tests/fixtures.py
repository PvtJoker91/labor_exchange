import asyncio
from typing import AsyncIterable
from unittest.mock import MagicMock

from dishka import provide, Scope
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from core.config import Settings
from di import AppProvider
from domain.entities.users import UserEntity


class MockSessionProvider(AppProvider):
    @provide(scope=Scope.APP)
    async def get_session(self, settings: Settings) -> AsyncIterable[AsyncSession]:
        engine = create_async_engine(settings.db.db_url)
        connection = await engine.connect()
        trans = await connection.begin()

        session_maker = async_sessionmaker(connection, expire_on_commit=False, class_=AsyncSession)
        session = session_maker()

        async def mock_delete(instance):
            session.expunge(instance)
            return await asyncio.sleep(0)

        session.commit = MagicMock(side_effect=session.flush)
        session.delete = MagicMock(side_effect=mock_delete)

        try:
            yield session
        finally:
            await session.close()
            await trans.rollback()
            await connection.close()
            await engine.dispose()


def mock_get_auth_user():
    return UserEntity(
        name='TestAuthUser',
        email='test_auth_user@ex.com',
        is_company=False,
    )
