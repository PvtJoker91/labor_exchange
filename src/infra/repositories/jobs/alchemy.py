from sqlalchemy import select, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from domain.entities.jobs import JobEntity
from infra.exceptions.jobs import JobNotFoundDBException
from infra.repositories.alchemy_models.jobs import Job
from infra.repositories.jobs.base import BaseJobRepository
from infra.repositories.jobs.converters import convert_job_entity_to_dto


class AlchemyJobRepository(BaseJobRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one_by_id(self, job_id: str) -> Job:
        query = select(Job).where(Job.id == job_id).limit(1)
        try:
            res = await self.session.execute(query)
            job = res.scalar_one()
        except NoResultFound:
            raise JobNotFoundDBException(job_id=job_id)
        return job

    async def get_all(self, limit: int, offset: int) -> list[Job]:
        query = select(Job).limit(limit).offset(offset)
        res = await self.session.execute(query)
        return res.scalars().all()

    async def add(self, job_in: JobEntity) -> Job:
        new_job = convert_job_entity_to_dto(job_in)
        self.session.add(new_job)
        await self.session.commit()
        await self.session.refresh(new_job)
        return new_job

    async def delete(self, job_id: str) -> None:
        query = delete(Job).where(Job.id == job_id)
        await self.session.execute(query)
        await self.session.commit()

