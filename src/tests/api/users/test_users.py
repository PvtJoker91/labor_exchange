import pytest
from httpx import Response
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.v1.users.schemas import UserInSchema, UserUpdateSchema
from domain.entities.users import UserEntity
from logic.services.users.repo import RepositoryUserService


@pytest.mark.asyncio
async def test_create_user(
        app: FastAPI,
        client: TestClient,
        new_user_schema: UserInSchema,
        user_entity: UserEntity,
        monkeypatch
):
    async def mock_create_user(*args, **kwargs):
        return user_entity

    monkeypatch.setattr(RepositoryUserService, "create_user", mock_create_user)
    url = app.url_path_for('create_user')
    response: Response = client.post(url=url, json=new_user_schema.model_dump())

    assert response.is_success


@pytest.mark.asyncio
async def test_read_users(
        app: FastAPI,
        client: TestClient,
        monkeypatch
):
    async def mock_read_users(*args, **kwargs):
        return []

    monkeypatch.setattr(RepositoryUserService, "get_user_list", mock_read_users)
    url = app.url_path_for('read_users')
    response: Response = client.get(url)

    assert response.is_success


@pytest.mark.asyncio
async def test_update_user(
        app: FastAPI,
        client: TestClient,
        user_to_update_schema: UserUpdateSchema,
        user_entity: UserEntity,
        monkeypatch
):
    async def mock_update_user(*args, **kwargs):
        return user_entity

    monkeypatch.setattr(RepositoryUserService, "update_user", mock_update_user)
    url = app.url_path_for('update_user', user_id="1")
    response: Response = client.patch(url=url, json=user_to_update_schema.model_dump())

    assert response.is_success
