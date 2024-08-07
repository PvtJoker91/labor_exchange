import pytest
from dishka.async_container import AsyncContainer

from domain.entities.jobs import JobEntity
from domain.entities.responses import ResponseEntity
from domain.entities.users import UserEntity
from infra.repositories.jobs.converters import convert_job_entity_to_dto

from infra.repositories.responses.alchemy import AlchemyResponseRepository
from infra.repositories.responses.converters import convert_response_entity_to_dto
from infra.repositories.users.converters import convert_user_entity_to_dto
from logic.exceptions.responses import OnlyNotCompanyUsersCanMakeResponsesException, OnlyUserCanGetTheirResponses, \
    OnlyCompanyCanGetTheirResponses

from logic.services.responses.base import BaseResponseService


@pytest.mark.asyncio
async def test_make_response(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = False
    response_entity = ResponseEntity(
        message="Test message",
        user_id="1",
        job_id="1",
    )

    async def mock_add_response(*args, **kwargs):
        return convert_response_entity_to_dto(response_entity)

    monkeypatch.setattr(AlchemyResponseRepository, "add", mock_add_response)
    async with mock_container() as container:
        service = await container.get(BaseResponseService)
        response = await service.make_response(response_entity, user_entity)
        assert response
        assert response.message == "Test message"


@pytest.mark.asyncio
async def test_make_response_company_error(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = True
    response_entity = ResponseEntity(
        message="Test message",
        user_id="1",
        job_id="1",
    )
    async with mock_container() as container:
        service = await container.get(BaseResponseService)
        with pytest.raises(OnlyNotCompanyUsersCanMakeResponsesException):
            await service.make_response(response_entity, user_entity)


@pytest.mark.asyncio
async def test_get_user_response_list(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = False
    response_entity = ResponseEntity(
        message="Test message",
        user_id="1",
        job_id="1",
    )
    job_entity = JobEntity(
        id="1",
        title="TestJob",
        description="Test Job Description",
        salary_from=100,
        salary_to=200,
        is_active=True,
        user_id="1",
    )

    async def mock_get_list_by_user_id(*args, **kwargs):
        response_dto = convert_response_entity_to_dto(response_entity)
        response_dto.job = convert_job_entity_to_dto(job_entity)
        return [response_dto]

    monkeypatch.setattr(AlchemyResponseRepository, "get_list_by_user_id", mock_get_list_by_user_id)
    async with mock_container() as container:
        service = await container.get(BaseResponseService)
        response_list = await service.get_user_response_list(user_entity)
        assert response_list
        assert response_list[0].message == "Test message"
        assert response_list[0].job.title == "TestJob"


@pytest.mark.asyncio
async def test_get_user_response_list_company_error(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = True
    async with mock_container() as container:
        service = await container.get(BaseResponseService)
        with pytest.raises(OnlyUserCanGetTheirResponses):
            await service.get_user_response_list(user_entity)


@pytest.mark.asyncio
async def test_get_company_response_list(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = True
    response_entity = ResponseEntity(
        message="Test message",
        user_id=user_entity.id,
        job_id="1",
    )

    async def mock_get_list_by_company_user_id(*args, **kwargs):
        response_dto = convert_response_entity_to_dto(response_entity)
        response_dto.user = convert_user_entity_to_dto(user_entity)
        return [response_dto]

    monkeypatch.setattr(AlchemyResponseRepository, "get_list_by_company_user_id", mock_get_list_by_company_user_id)
    async with mock_container() as container:
        service = await container.get(BaseResponseService)
        response_list = await service.get_company_response_list(user_entity)
        assert response_list
        assert response_list[0].message == "Test message"
        assert response_list[0].user.name == user_entity.name


@pytest.mark.asyncio
async def test_get_company_response_list_not_company_error(
        mock_container: AsyncContainer,
        user_entity: UserEntity,
        monkeypatch,
):
    user_entity.is_company = False
    async with mock_container() as container:
        service = await container.get(BaseResponseService)
        with pytest.raises(OnlyCompanyCanGetTheirResponses):
            await service.get_company_response_list(user_entity)