from uuid import uuid4

import factory

from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from infra.repositories.alchemy_models.users import User


class UserFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = User

    id = str(uuid4())
    name = factory.Faker("pystr")
    email = factory.Faker("email")
    hashed_password = b"asdsadasd"
    is_company = factory.Faker("pybool")
    created_at = factory.LazyFunction(datetime.now)
