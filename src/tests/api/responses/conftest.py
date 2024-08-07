import pytest

from api.v1.responses.schemas import ResponseCreateSchema
from domain.entities.jobs import JobEntity
from domain.entities.responses import ResponseAggregateJobEntity, ResponseAggregateUserEntity, ResponseEntity


@pytest.fixture
def response_entity():
    return ResponseEntity(
        message="TestResponse",
        user_id="user_id",
        job_id="job_id",
    )


@pytest.fixture
def response_job_entity():
    return ResponseAggregateJobEntity(
        message="TestResponse",
        user_id="user_id",
        job_id="job_id",
        job=JobEntity(
            title="TestJob",
            description="TestJobDescription",
            salary_from=1000,
            salary_to=2000,
            is_active=True,
            user_id="user_id",
        )
    )


@pytest.fixture
def response_user_entity(user_entity):
    return ResponseAggregateUserEntity(
        message="TestResponse",
        user_id="user_id",
        job_id="job_id",
        user=user_entity
    )


@pytest.fixture
def new_response_schema():
    return ResponseCreateSchema(
        message="TestResponse",
        user_id="user_id",
        job_id="job_id",
    )
