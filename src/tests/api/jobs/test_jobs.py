import pytest
from httpx import Response
from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.v1.jobs.schemas import JobCreateSchema
from domain.entities.jobs import JobEntity
from logic.services.jobs.repo import RepositoryJobService


@pytest.mark.asyncio
async def test_create_job(
        app: FastAPI,
        client: TestClient,
        new_job_schema: JobCreateSchema,
        job_entity: JobEntity,
        monkeypatch
):
    async def mock_create_job(*args, **kwargs):
        return job_entity

    monkeypatch.setattr(RepositoryJobService, "create_job", mock_create_job)
    url = app.url_path_for('create_job')
    response: Response = client.post(url=url, json=new_job_schema.model_dump())

    assert response.is_success


@pytest.mark.asyncio
async def test_get_all_jobs(
        app: FastAPI,
        client: TestClient,
        job_entity: JobEntity,
        monkeypatch
):
    async def mock_read_jobs(*args, **kwargs):
        return [job_entity]

    monkeypatch.setattr(RepositoryJobService, "get_job_list", mock_read_jobs)
    url = app.url_path_for('get_all_jobs')
    response: Response = client.get(url)

    assert response.is_success


@pytest.mark.asyncio
async def test_get_job_by_id(
        app: FastAPI,
        client: TestClient,
        job_entity: JobEntity,
        monkeypatch
):
    async def mock_get_job(*args, **kwargs):
        return job_entity

    monkeypatch.setattr(RepositoryJobService, "get_job_by_id", mock_get_job)
    url = app.url_path_for('get_job_by_id', job_id="1")
    response: Response = client.get(url=url)

    assert response.is_success


@pytest.mark.asyncio
async def test_delete_job(
        app: FastAPI,
        client: TestClient,
        monkeypatch
):
    async def mock_delete_job(*args, **kwargs):
        return None

    monkeypatch.setattr(RepositoryJobService, "delete_job", mock_delete_job)
    url = app.url_path_for('delete_job', job_id="1")
    response: Response = client.delete(url=url)

    assert response.is_success
