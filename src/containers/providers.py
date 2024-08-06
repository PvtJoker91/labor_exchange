from typing import AsyncIterable

from dishka import Provider, provide, Scope, from_context
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from core.config import Settings
from infra.repositories.jobs.alchemy import AlchemyJobRepository
from infra.repositories.jobs.base import BaseJobRepository
from infra.repositories.responses.alchemy import AlchemyResponseRepository
from infra.repositories.responses.base import BaseResponseRepository

from infra.repositories.session import new_session_maker
from infra.repositories.users.alchemy import AlchemyUserRepository
from infra.repositories.users.base import BaseUserRepository
from logic.services.auth.jwt_auth import JWTAuthService
from logic.services.jobs.base import BaseJobService
from logic.services.jobs.repo import RepositoryJobService
from logic.services.responses.base import BaseResponseService
from logic.services.responses.repo import RepositoryResponseService
from logic.services.users.base import BaseUserService
from logic.services.users.repo import RepositoryUserService


class AppProvider(Provider):
    settings = from_context(provides=Settings, scope=Scope.APP)

    @provide(scope=Scope.APP)
    def get_session_maker(self, settings: Settings) -> async_sessionmaker[AsyncSession]:
        return new_session_maker(settings.db.db_url)

    @provide(scope=Scope.REQUEST)
    async def get_session(self, session_maker: async_sessionmaker[AsyncSession]) -> AsyncIterable[AsyncSession]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    def get_user_repository(self, session: AsyncSession) -> BaseUserRepository:
        return AlchemyUserRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_job_repository(self, session: AsyncSession) -> BaseJobRepository:
        return AlchemyJobRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_response_repository(self, session: AsyncSession) -> BaseResponseRepository:
        return AlchemyResponseRepository(session)

    @provide(scope=Scope.REQUEST)
    def get_user_service(self, user_repository: BaseUserRepository) -> BaseUserService:
        return RepositoryUserService(user_repository)

    @provide(scope=Scope.REQUEST)
    def get_auth_service(self, user_repository: BaseUserRepository) -> JWTAuthService:
        return JWTAuthService(user_repository)

    @provide(scope=Scope.REQUEST)
    def get_job_service(self, job_repository: BaseJobRepository) -> BaseJobService:
        return RepositoryJobService(job_repository)

    @provide(scope=Scope.REQUEST)
    def get_response_service(
            self,
            response_repository: BaseResponseRepository,
            job_repository: BaseJobRepository
    ) -> BaseResponseService:
        return RepositoryResponseService(response_repository, job_repository)
