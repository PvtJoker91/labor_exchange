import pytest
from httpx import Response
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.v1.responses.schemas import ResponseCreateSchema
from domain.entities.responses import ResponseEntity, ResponseAggregateJobEntity, ResponseAggregateUserEntity
from logic.services.responses.repo import RepositoryResponseService


@pytest.mark.asyncio
async def test_make_response(
        app: FastAPI,
        client: TestClient,
        new_response_schema: ResponseCreateSchema,
        response_entity: ResponseEntity,
        monkeypatch
):
    async def mock_make_response(*args, **kwargs):
        return response_entity

    monkeypatch.setattr(RepositoryResponseService, "make_response", mock_make_response)
    url = app.url_path_for('make_response')
    response: Response = client.post(url=url, json=new_response_schema.model_dump())

    assert response.is_success


@pytest.mark.asyncio
async def test_get_all_user_responses(
        app: FastAPI,
        client: TestClient,
        response_job_entity: ResponseAggregateJobEntity,
        monkeypatch
):
    async def mock_get_responses(*args, **kwargs):
        return [response_job_entity]

    monkeypatch.setattr(RepositoryResponseService, "get_user_response_list", mock_get_responses)
    url = app.url_path_for('get_all_user_responses')
    response: Response = client.get(url)

    assert response.is_success


@pytest.mark.asyncio
async def test_get_all_company_responses(
        app: FastAPI,
        client: TestClient,
        response_user_entity: ResponseAggregateUserEntity,
        monkeypatch
):
    async def mock_get_responses(*args, **kwargs):
        return [response_user_entity]

    monkeypatch.setattr(RepositoryResponseService, "get_company_response_list", mock_get_responses)
    url = app.url_path_for('get_all_company_responses')
    response: Response = client.get(url)

    assert response.is_success


@pytest.mark.asyncio
async def test_get_all_job_responses(
        app: FastAPI,
        client: TestClient,
        response_user_entity: ResponseAggregateUserEntity,
        monkeypatch
):
    async def mock_get_responses(*args, **kwargs):
        return [response_user_entity]

    monkeypatch.setattr(RepositoryResponseService, "get_job_response_list", mock_get_responses)
    url = app.url_path_for('get_all_job_responses')
    response: Response = client.get(url, params={"job_id": "1"})

    assert response.is_success


@pytest.mark.asyncio
async def test_delete_response(
        app: FastAPI,
        client: TestClient,
        monkeypatch
):
    async def mock_delete_response(*args, **kwargs):
        return None

    monkeypatch.setattr(RepositoryResponseService, "delete_response", mock_delete_response)
    url = app.url_path_for('delete_response', response_id="1")
    response: Response = client.delete(url=url)

    assert response.is_success
