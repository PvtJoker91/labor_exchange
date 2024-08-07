import pytest

from dishka.async_container import AsyncContainer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.jobs import JobEntity
from infra.exceptions.jobs import JobNotFoundDBException
from infra.repositories.alchemy_models.jobs import Job
from infra.repositories.jobs.base import BaseJobRepository
from tests.repositories.fixtures import UserFactory, JobFactory


@pytest.mark.asyncio
async def test_get_all(mock_container: AsyncContainer):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        repo = await container.get(BaseJobRepository)
        all_jobs = await repo.get_all(limit=100, offset=0)
        assert all_jobs
        assert job in all_jobs


@pytest.mark.asyncio
async def test_get_one_by_id(mock_container: AsyncContainer):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        new_job = JobFactory.build(user_id=user.id)
        session.add(new_job)
        await session.flush()

        repo = await container.get(BaseJobRepository)
        job = await repo.get_one_by_id(new_job.id)
        assert job is not None
        assert job.id == new_job.id


@pytest.mark.asyncio
async def test_get_one_by_wrong_id_error(mock_container: AsyncContainer):
    async with mock_container() as container:
        repo = await container.get(BaseJobRepository)
        with pytest.raises(JobNotFoundDBException):
            await repo.get_one_by_id("wrong_id")


@pytest.mark.asyncio
async def test_add(mock_container: AsyncContainer):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        new_job = JobEntity(
            title="TestJob",
            description="TestDescr",
            salary_from=100,
            salary_to=200,
            is_active=True,
            user_id=user.id,

        )
        repo = await container.get(BaseJobRepository)
        created_job = await repo.add(job_in=new_job)
        assert created_job is not None
        assert created_job.title == new_job.title
        assert created_job.user_id == new_job.user_id


@pytest.mark.asyncio
async def test_delete(mock_container: AsyncContainer):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        query = select(Job).where(Job.id == job.id)

        res = await session.execute(query)
        job_to_delete = res.scalar()

        assert job_to_delete

        repo = await container.get(BaseJobRepository)
        await repo.delete(job_id=job.id)

        res = await session.execute(query)
        job_to_delete = res.scalar()

        assert not job_to_delete
