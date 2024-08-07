import pytest

from api.v1.auth.schemas import LoginSchema, RefreshTokenSchema
from domain.entities.auth import TokenEntity, TokenPayloadEntity


@pytest.fixture
def token_entity():
    return TokenEntity(
        access_token="test_access",
        refresh_token="test_refresh",
        token_type="Bearer"
    )


@pytest.fixture
def payload_entity():
    return TokenPayloadEntity(
        sub="test_user@mail.ru",
    )


@pytest.fixture
def login_schema():
    return LoginSchema(
        email="test_user@mail.ru",
        password="test_pass",
    )


@pytest.fixture
def refresh_schema():
    return RefreshTokenSchema(
        refresh_token="test_refresh",
    )
