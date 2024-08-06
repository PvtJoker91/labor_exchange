import pytest
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.responses import ResponseEntity
from infra.exceptions.responses import ResponseNotFoundDBException
from infra.repositories.alchemy_models.responses import Response
from infra.repositories.responses.base import BaseResponseRepository
from tests.repositories.fixtures import UserFactory, JobFactory, ResponseFactory


@pytest.mark.asyncio
async def test_add_response(mock_container):
    async with mock_container() as container:
        session = await container.get(AsyncSession)

        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        new_response = ResponseEntity(
            message="TestMessage",
            user_id=user.id,
            job_id=job.id
        )

        repo = await container.get(BaseResponseRepository)
        created_response = await repo.add(new_response)
        assert created_response.id == new_response.id
        assert created_response.message == new_response.message


@pytest.mark.asyncio
async def test_get_one_response_by_id(mock_container):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        new_response = ResponseFactory.build(user_id=user.id, job_id=job.id)
        session.add(new_response)
        await session.flush()

        repo = await container.get(BaseResponseRepository)
        response = await repo.get_one_by_id(new_response.id)
        assert response.id == new_response.id


@pytest.mark.asyncio
async def test_get_one_response_by_wrong_id_error(mock_container):
    async with mock_container() as container:
        repo = await container.get(BaseResponseRepository)
        with pytest.raises(ResponseNotFoundDBException):
            await repo.get_one_by_id("wrong_id")


@pytest.mark.asyncio
async def test_get_one_response_by_id_join_job(mock_container):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        new_response = ResponseFactory.build(user_id=user.id, job_id=job.id)
        session.add(new_response)
        await session.flush()

        repo = await container.get(BaseResponseRepository)
        response = await repo.get_one_by_id(new_response.id)
        assert response.id == new_response.id
        assert response.job.title == new_response.job.title


@pytest.mark.asyncio
async def test_get_response_list_by_user_id(mock_container):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        response = ResponseFactory.build(user_id=user.id, job_id=job.id)
        session.add(response)
        await session.flush()

        repo = await container.get(BaseResponseRepository)
        response_list = await repo.get_list_by_user_id(user.id)

        assert response_list
        assert response_list[0] == response


@pytest.mark.asyncio
async def test_get_response_list_by_company_user_id(mock_container):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        response = ResponseFactory.build(user_id=user.id, job_id=job.id)
        session.add(response)
        await session.flush()

        repo = await container.get(BaseResponseRepository)
        response_list = await repo.get_list_by_company_user_id(user.id)

        assert response_list
        assert response_list[0] == response


@pytest.mark.asyncio
async def test_get_response_list_by_job_id(mock_container):
    async with mock_container() as container:
        session = await container.get(AsyncSession)

        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        response = ResponseFactory.build(user_id=user.id, job_id=job.id)
        session.add(response)
        await session.flush()

        repo = await container.get(BaseResponseRepository)
        response_list = await repo.get_list_by_job_id(job.id)

        assert response_list
        assert response_list[0] == response


@pytest.mark.asyncio
async def test_delete_response(mock_container):
    async with mock_container() as container:
        session = await container.get(AsyncSession)
        user = UserFactory.build()
        session.add(user)
        await session.flush()

        job = JobFactory.build(user_id=user.id)
        session.add(job)
        await session.flush()

        response = ResponseFactory.build(user_id=user.id, job_id=job.id)
        session.add(response)
        await session.flush()

        query = select(Response).where(Response.id == response.id)

        res = await session.execute(query)
        response_to_delete = res.scalar()
        assert response_to_delete

        repo = await container.get(BaseResponseRepository)
        await repo.delete(response_id=response.id)

        res = await session.execute(query)
        response_to_delete = res.scalar()
        assert not response_to_delete
