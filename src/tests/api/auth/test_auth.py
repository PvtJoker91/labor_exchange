import pytest
from httpx import Response
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.v1.auth.schemas import LoginSchema, RefreshTokenSchema
from domain.entities.auth import TokenEntity, TokenPayloadEntity
from domain.entities.users import UserEntity
from logic.services.auth.jwt_auth import JWTAuthService
from logic.services.users.repo import RepositoryUserService


@pytest.mark.asyncio
async def test_login(
        app: FastAPI,
        client: TestClient,
        login_schema: LoginSchema,
        token_entity: TokenEntity,
        monkeypatch
):
    async def mock_login(*args, **kwargs):
        return token_entity

    monkeypatch.setattr(JWTAuthService, "login_user", mock_login)
    url = app.url_path_for('login')
    response: Response = client.post(url=url, json=login_schema.model_dump())

    assert response.is_success


@pytest.mark.asyncio
async def test_refresh(
        app: FastAPI,
        client: TestClient,
        user_entity: UserEntity,
        payload_entity: TokenPayloadEntity,
        refresh_schema: RefreshTokenSchema,
        monkeypatch
):
    def mock_get_token_payload(*args, **kwargs):
        return payload_entity

    def mock_create_token(*args, **kwargs):
        return "test_token"

    async def mock_get_user(*args, **kwargs):
        return user_entity

    monkeypatch.setattr(JWTAuthService, "get_token_payload", mock_get_token_payload)
    monkeypatch.setattr(JWTAuthService, "create_access_token", mock_create_token)
    monkeypatch.setattr(JWTAuthService, "create_refresh_token", mock_create_token)
    monkeypatch.setattr(RepositoryUserService, "get_user_by_email", mock_get_user)

    url = app.url_path_for('refresh_token')
    response: Response = client.post(url, json=refresh_schema.model_dump())

    assert response.is_success
