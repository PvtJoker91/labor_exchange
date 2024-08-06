import pytest
from dishka.async_container import AsyncContainer

from domain.entities.jobs import JobEntity
from domain.entities.users import UserEntity

from infra.repositories.jobs.alchemy import AlchemyJobRepository
from infra.repositories.jobs.converters import convert_job_entity_to_dto
from logic.exceptions.jobs import OnlyCompanyCanCreateJobException, OnlyJobOwnerCanDeleteJobException

from logic.services.jobs.base import BaseJobService


@pytest.mark.asyncio
async def test_get_job_by_id(
        mock_container: AsyncContainer,
        monkeypatch,
):
    job_entity = JobEntity(
        title="TestJob",
        description="Test Job Description",
        salary_from=100,
        salary_to=200,
        is_active=True,
        user_id="1",

    )

    async def mock_get_job_by_id(*args, **kwargs):
        return convert_job_entity_to_dto(job_entity)

    monkeypatch.setattr(AlchemyJobRepository, "get_one_by_id", mock_get_job_by_id)
    async with mock_container() as container:
        service = await container.get(BaseJobService)
        job = await service.get_job_by_id(job_id="1")
        assert job
        assert job.title == "TestJob"


@pytest.mark.asyncio
async def test_get_job_list(
        mock_container: AsyncContainer,
        monkeypatch,
):
    job_entity = JobEntity(
        title="TestJob",
        description="Test Job Description",
        salary_from=100,
        salary_to=200,
        is_active=True,
        user_id="1",

    )

    async def mock_get_job_by_id(*args, **kwargs):
        return [convert_job_entity_to_dto(job_entity)]

    monkeypatch.setattr(AlchemyJobRepository, "get_all", mock_get_job_by_id)
    async with mock_container() as container:
        service = await container.get(BaseJobService)
        job_list = await service.get_job_list(limit=20, offset=0)
        assert job_list
        assert job_list[0].title == "TestJob"


@pytest.mark.asyncio
async def test_create_job(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = True
    job_entity = JobEntity(
        title="TestJob",
        description="Test Job Description",
        salary_from=100,
        salary_to=200,
        is_active=True,
        user_id=user_entity.id,

    )

    async def mock_create_job(*args, **kwargs):
        return convert_job_entity_to_dto(job_entity)

    monkeypatch.setattr(AlchemyJobRepository, "add", mock_create_job)
    async with mock_container() as container:
        service = await container.get(BaseJobService)
        job = await service.create_job(job_entity, user_entity)
        assert job
        assert job.title == "TestJob"


@pytest.mark.asyncio
async def test_create_job_not_company_error(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = False
    job_entity = JobEntity(
        title="TestJob",
        description="Test Job Description",
        salary_from=100,
        salary_to=200,
        is_active=True,
        user_id=user_entity.id,

    )

    async def mock_create_job(*args, **kwargs):
        return convert_job_entity_to_dto(job_entity)

    monkeypatch.setattr(AlchemyJobRepository, "add", mock_create_job)
    async with mock_container() as container:
        service = await container.get(BaseJobService)
        with pytest.raises(OnlyCompanyCanCreateJobException):
            await service.create_job(job_entity, user_entity)


@pytest.mark.asyncio
async def test_delete_job(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = True
    job_entity = JobEntity(
        title="TestJob",
        description="Test Job Description",
        salary_from=100,
        salary_to=200,
        is_active=True,
        user_id=user_entity.id,

    )

    async def mock_get_one_by_id(*args, **kwargs):
        return convert_job_entity_to_dto(job_entity)

    async def mock_delete_job(*args, **kwargs):
        return None

    monkeypatch.setattr(AlchemyJobRepository, "get_one_by_id", mock_get_one_by_id)
    monkeypatch.setattr(AlchemyJobRepository, "delete", mock_delete_job)
    async with mock_container() as container:
        service = await container.get(BaseJobService)
        await service.delete_job(job_id="1", user=user_entity)


@pytest.mark.asyncio
async def test_delete_job_not_job_owner_error(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = True
    job_entity = JobEntity(
        title="TestJob",
        description="Test Job Description",
        salary_from=100,
        salary_to=200,
        is_active=True,
        user_id="different_id",

    )

    async def mock_get_one_by_id(*args, **kwargs):
        return convert_job_entity_to_dto(job_entity)

    async def mock_delete_job(*args, **kwargs):
        return None

    monkeypatch.setattr(AlchemyJobRepository, "get_one_by_id", mock_get_one_by_id)
    monkeypatch.setattr(AlchemyJobRepository, "delete", mock_delete_job)
    async with mock_container() as container:
        service = await container.get(BaseJobService)
        with pytest.raises(OnlyJobOwnerCanDeleteJobException):
            await service.delete_job(job_id="1", user=user_entity)
