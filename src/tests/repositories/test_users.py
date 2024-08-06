import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from domain.entities.users import UserEntity
from infra.exceptions.users import UserAlreadyExistsDBException
from infra.repositories.users.base import BaseUserRepository
from infra.repositories.users.converters import convert_user_entity_to_dto
from tests.repositories.fixtures import UserFactory


@pytest.mark.asyncio
async def test_get_all(container):
    async with container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        repo = await container.get(BaseUserRepository)
        all_users = await repo.get_all(limit=100, offset=0)
        assert all_users
        assert user in all_users


@pytest.mark.asyncio
async def test_get_by_id(container):
    async with container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        repo = await container.get(BaseUserRepository)
        current_user = await repo.get_one_by_id(user.id)
        assert current_user is not None
        assert current_user.id == user.id


@pytest.mark.asyncio
async def test_get_one_by_email(container):
    async with container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        repo = await container.get(BaseUserRepository)
        current_user = await repo.get_one_by_email(user.email)
        assert current_user is not None
        assert current_user.id == user.id


@pytest.mark.asyncio
async def test_create(container):
    user = UserEntity(
        name="Uchpochmak",
        email="bashkort@example.com",
        hashed_password=b"eshkere!",
        is_company=False
    )
    async with container() as container:
        repo = await container.get(BaseUserRepository)
        new_user = await repo.add(user_in=user)
        assert new_user is not None
        assert new_user.name == "Uchpochmak"
        assert new_user.hashed_password == b"eshkere!"


@pytest.mark.asyncio
async def test_update(container):
    async with container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        repo = await container.get(BaseUserRepository)
        entity = user.to_entity()
        entity.name = "updated_name"
        updated_user = await repo.update(user_in=entity)
        assert user.id == updated_user.id
        assert updated_user.name == "updated_name"


@pytest.mark.asyncio
async def test_create_same_email_error(container):
    user = UserEntity(
        name="Uchpochmak",
        email="bashkort@example.com",
        hashed_password=b"eshkere!",
        is_company=False
    )
    async with container() as container:
        session = await container.get(AsyncSession)
        session.add(convert_user_entity_to_dto(user))
        await session.flush()
        repo = await container.get(BaseUserRepository)
        with pytest.raises(UserAlreadyExistsDBException):
            await repo.add(user_in=user)
