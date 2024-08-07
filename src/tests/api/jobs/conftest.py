import pytest

from api.v1.jobs.schemas import JobCreateSchema
from domain.entities.jobs import JobEntity


@pytest.fixture
def job_entity():
    return JobEntity(
        title="TestJob",
        description="TestJobDescription",
        salary_from=1000,
        salary_to=2000,
        is_active=True,
        user_id="user_id",
    )


@pytest.fixture
def new_job_schema():
    return JobCreateSchema(
        title="TestJob",
        description="TestJobDescription",
        salary_from=1000,
        salary_to=2000,
        is_active=True,
        user_id="user_id",
    )
