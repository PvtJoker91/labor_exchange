import pytest
from dishka.async_container import AsyncContainer

from domain.entities.users import UserEntity
from infra.repositories.users.alchemy import AlchemyUserRepository
from infra.repositories.users.converters import convert_user_entity_to_dto
from logic.exceptions.users import UpdateOtherUserException

from logic.services.users.base import BaseUserService


@pytest.mark.asyncio
async def test_get_user_list(
        mock_container: AsyncContainer,
        monkeypatch
):
    user_entity = UserEntity(
        name="TestUser",
        email="test_user@mail.ru",
        password="test_pass",
        is_company=False,
    )

    async def mock_get_all(*args, **kwargs):
        return [convert_user_entity_to_dto(user_entity)]

    monkeypatch.setattr(AlchemyUserRepository, "get_all", mock_get_all)
    async with mock_container() as container:
        service = await container.get(BaseUserService)
        user_list = await service.get_user_list(limit=20, offset=0)

        assert user_list
        assert user_list[0].id == user_entity.id


@pytest.mark.asyncio
async def test_get_user_by_email(
        mock_container: AsyncContainer,
        monkeypatch
):
    user_entity = UserEntity(
        name="TestUser",
        email="test_user@mail.ru",
        password="test_pass",
        is_company=False,
    )

    async def mock_get_by_email(*args, **kwargs):
        return convert_user_entity_to_dto(user_entity)

    monkeypatch.setattr(AlchemyUserRepository, "get_one_by_email", mock_get_by_email)
    async with mock_container() as container:
        service = await container.get(BaseUserService)
        user = await service.get_user_by_email(user_entity.email)

        assert user
        assert user.id == user_entity.id


@pytest.mark.asyncio
async def test_create_user(
        mock_container: AsyncContainer,
        monkeypatch
):
    user_entity = UserEntity(
        name="TestUser",
        email="test_user@mail.ru",
        password="test_pass",
        is_company=False,
    )

    async def mock_add(*args, **kwargs):
        return convert_user_entity_to_dto(user_entity)

    monkeypatch.setattr(AlchemyUserRepository, "add", mock_add)
    async with mock_container() as container:
        service = await container.get(BaseUserService)
        user = await service.create_user(user_entity)

        assert user
        assert user.id == user_entity.id
        assert user.name == "TestUser"


@pytest.mark.asyncio
async def test_update_user(
        mock_container: AsyncContainer,
        monkeypatch
):
    user_entity = UserEntity(
        name="TestUser",
        email="test_user@mail.ru",
        password="test_pass",
        is_company=False,
    )

    async def mock_get_one_by_id(*args, **kwargs):
        return convert_user_entity_to_dto(user_entity)

    async def mock_update(*args, **kwargs):
        user_entity.name = "NewName"
        return convert_user_entity_to_dto(user_entity)

    monkeypatch.setattr(AlchemyUserRepository, "get_one_by_id", mock_get_one_by_id)
    monkeypatch.setattr(AlchemyUserRepository, "update", mock_update)
    async with mock_container() as container:
        service = await container.get(BaseUserService)
        upd_user = await service.update_user(
            user_id=user_entity.id,
            user_in=user_entity,
            auth_user_email=user_entity.email,
        )

        assert upd_user
        assert upd_user.name == "NewName"


@pytest.mark.asyncio
async def test_update_user_wrong_email_error(
        mock_container: AsyncContainer,
        monkeypatch
):
    user_entity = UserEntity(
        name="TestUser",
        email="test_user@mail.ru",
        password="test_pass",
        is_company=False,
    )

    async def mock_get_one_by_id(*args, **kwargs):
        user_entity.email = "different@mail.com"
        return convert_user_entity_to_dto(user_entity)

    async def mock_update(*args, **kwargs):
        return convert_user_entity_to_dto(user_entity)

    monkeypatch.setattr(AlchemyUserRepository, "get_one_by_id", mock_get_one_by_id)
    monkeypatch.setattr(AlchemyUserRepository, "update", mock_update)
    async with mock_container() as container:
        service = await container.get(BaseUserService)
        with pytest.raises(UpdateOtherUserException):
            await service.update_user(user_id=user_entity.id, user_in=user_entity, auth_user_email="test_user@mail.ru")
