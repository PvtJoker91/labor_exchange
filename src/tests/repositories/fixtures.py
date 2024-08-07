from uuid import uuid4

import factory

from datetime import datetime
from factory_boy_extra.async_sqlalchemy_factory import AsyncSQLAlchemyModelFactory

from infra.repositories.alchemy_models.jobs import Job
from infra.repositories.alchemy_models.responses import Response
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


class JobFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Job

    id = str(uuid4())
    title = factory.Faker('job')
    description = factory.Faker('paragraph', nb_sentences=3)
    salary_from = factory.Faker('pyint', min_value=100, max_value=1000000)
    salary_to = factory.LazyAttribute(lambda x: x.salary_from * 1.1)
    is_active = factory.Faker('pybool')


class ResponseFactory(AsyncSQLAlchemyModelFactory):
    class Meta:
        model = Response

    id = str(uuid4())
    message = factory.Faker('paragraph', nb_sentences=3)
