import pytest

from api.v1.users.schemas import UserInSchema, UserUpdateSchema


@pytest.fixture
def new_user():
    return UserInSchema(
        name="TestUser",
        email="test_not_company_user@mail.ru",
        password="test_pass",
        password2="test_pass",
        is_company=False,
    )


@pytest.fixture
def new_company_user():
    return UserInSchema(
        name="TestCompanyUser",
        email="test_company_user@mail.ru",
        password="test_pass",
        password2="test_pass",
        is_company=True,
    )


@pytest.fixture
def user_to_update():
    return UserUpdateSchema(
        name="NewNameTestCompanyUser",
    )
