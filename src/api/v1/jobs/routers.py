from fastapi import APIRouter, Depends, HTTPException, status
from dishka.integrations.fastapi import inject, FromDishka

from api.v1.jobs.schemas import JobCreateSchema, JobSchema
from core.exceptions import ApplicationException
from api.dependencies.auth import get_auth_user
from domain.entities.users import UserEntity
from logic.services.jobs.base import BaseJobService

router = APIRouter(prefix="/jobs", tags=["jobs"])


@router.get("", response_model=list[JobSchema])
@inject
async def get_all_jobs(
        job_service: FromDishka[BaseJobService],
        limit: int = 100,
        offset: int = 0
) -> list[JobSchema]:
    jobs = await job_service.get_job_list(limit=limit, offset=offset)
    return [JobSchema.from_entity(job) for job in jobs]


@router.post("", response_model=JobSchema)
@inject
async def create_job(
        job_in: JobCreateSchema,
        job_service: FromDishka[BaseJobService],
        auth_user: UserEntity = Depends(get_auth_user),
) -> JobSchema:
    job_in.user_id = auth_user.id
    try:
        job = await job_service.create_job(job_in=job_in.to_entity(), auth_user=auth_user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=e.message,
        )
    return JobSchema.from_entity(job)


@router.put("", response_model=JobSchema)
@inject
async def get_job_by_id(
        job_id: str,
        job_service: FromDishka[BaseJobService],
) -> JobSchema:
    try:
        job = await job_service.get_job_by_id(job_id=job_id)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    return JobSchema.from_entity(job)


@router.delete("", status_code=status.HTTP_204_NO_CONTENT)
@inject
async def delete_job(
        job_id: str,
        job_service: FromDishka[BaseJobService],
        auth_user: UserEntity = Depends(get_auth_user),
) -> None:
    try:
        await job_service.delete_job(job_id=job_id, user=auth_user)
    except ApplicationException as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
