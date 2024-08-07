import pytest

from api.v1.users.schemas import UserInSchema, UserUpdateSchema


@pytest.fixture
def new_user_schema():
    return UserInSchema(
        name="TestUser",
        email="test_user@mail.ru",
        password="test_pass",
        password2="test_pass",
        is_company=False,
    )


@pytest.fixture
def user_to_update_schema():
    return UserUpdateSchema(
        name="NewNameTestCompanyUser",
    )
