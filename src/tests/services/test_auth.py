import pytest
from dishka.async_container import AsyncContainer

from domain.entities.users import UserEntity
from infra.repositories.alchemy_models.users import User
from infra.repositories.users.alchemy import AlchemyUserRepository
from logic.exceptions.auth import WrongCredentialsException
from logic.services.auth.jwt_auth import JWTAuthService
from logic.utils.auth import hash_password


@pytest.mark.asyncio
async def test_create_access_token(
        user_entity: UserEntity,
        mock_container: AsyncContainer
):
    async with mock_container() as container:
        service = await container.get(JWTAuthService)
        token = service.create_access_token(user_entity)
        assert token


@pytest.mark.asyncio
async def test_create_refresh_token(
        user_entity: UserEntity,
        mock_container: AsyncContainer
):
    async with mock_container() as container:
        service = await container.get(JWTAuthService)
        token = service.create_refresh_token(user_entity)
        assert token


@pytest.mark.asyncio
async def test_login_user(
        mock_container: AsyncContainer,
        monkeypatch
):
    async def mock_get_user(*args, **kwargs):
        return User(
            email="test@ex.com",
            name="test_name",
            hashed_password=hash_password("test_pass"),
            is_company=False
        )

    monkeypatch.setattr(AlchemyUserRepository, "get_one_by_email", mock_get_user)

    async with mock_container() as container:
        service = await container.get(JWTAuthService)
        token = await service.login_user("test@ex.com", "test_pass")
        assert token


@pytest.mark.asyncio
async def test_login_user_wrong_creds_error(
        mock_container: AsyncContainer,
        monkeypatch
):
    async def mock_get_user(*args, **kwargs):
        return User(
            email="test@ex.com",
            name="test_name",
            hashed_password=hash_password("test_pass"),
            is_company=False
        )

    monkeypatch.setattr(AlchemyUserRepository, "get_one_by_email", mock_get_user)

    async with mock_container() as container:
        service = await container.get(JWTAuthService)
        with pytest.raises(WrongCredentialsException):
            await service.login_user("test@ex.com", "wrong_pass")
