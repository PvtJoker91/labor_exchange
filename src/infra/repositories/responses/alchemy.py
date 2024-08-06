from sqlalchemy import select, delete
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound

from domain.entities.responses import ResponseEntity
from infra.exceptions.base import RepositoryException
from infra.exceptions.responses import ResponseNotFoundDBException
from infra.repositories.alchemy_models.jobs import Job
from infra.repositories.alchemy_models.responses import Response
from infra.repositories.responses.base import BaseResponseRepository
from infra.repositories.responses.converters import convert_response_entity_to_dto


class AlchemyResponseRepository(BaseResponseRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add(self, response_in: ResponseEntity) -> Response:
        new_response = convert_response_entity_to_dto(response_in)
        try:
            self.session.add(new_response)
            await self.session.commit()
        except IntegrityError:
            raise RepositoryException
        return new_response

    async def get_one_by_id(self, response_id: str) -> Response:
        query = select(Response).where(Response.id == response_id)
        try:
            res = await self.session.execute(query)
            response = res.scalar_one()
        except NoResultFound:
            raise ResponseNotFoundDBException(response_id=response_id)
        return response

    async def get_one_by_id_join_job(self, response_id: str) -> Response:
        query = select(Response).where(Response.id == response_id).options(joinedload(Response.job))
        try:
            res = await self.session.execute(query)
            response = res.scalar_one()
        except NoResultFound:
            raise ResponseNotFoundDBException(response_id=response_id)
        return response

    async def get_list_by_user_id(self, user_id: str) -> list[Response]:
        query = select(Response).where(Response.user_id == user_id).options(
                joinedload(Response.job)
            )
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_list_by_company_user_id(self, user_id: str) -> list[Response]:
        query = select(Response).join(Job).filter(Job.user_id == user_id).options(
                joinedload(Response.user)
            )
        res = await self.session.execute(query)
        return res.scalars().all()

    async def get_list_by_job_id(self, job_id: str) -> list[Response]:
        query = select(Response).where(Response.job_id == job_id).options(
                joinedload(Response.user)
            )
        res = await self.session.execute(query)
        return res.scalars().all()

    async def delete(self, response_id: str) -> None:
        query = delete(Response).where(Response.id == response_id)
        await self.session.execute(query)
        await self.session.commit()
